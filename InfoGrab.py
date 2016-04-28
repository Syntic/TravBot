import requests
from bs4 import BeautifulSoup
import time
import re
import Database
import sys


def set_server(server,domain):
    # Generate new URL
    url = 'http://' + server + '.travian.' + domain + '/'
    return url

def login(page, server, username, password):

    # Generate new URL
    url = server + '/' + page

    # Open session & add user agent
    s = requests.session()
    s.headers.update({'user-agent': 'Mozilla/5.0'})

    # Set Login Data
    login_data = dict(name=username, password=password, s1='Einloggen', login=time.time())
    # Send login data to login page
    s.post(url, data=login_data)
    # return session
    return s

def get_dorf1(session, server):

    # Grab dorf1.php
    text = session.get(server + '/' + 'dorf1.php')
    # Into BS
    soup = BeautifulSoup(text.content, 'lxml')

    ### Resources and Productions

    #Search for the resources block
    for hit in soup.find_all('script'):
        #Convert list to string
        str = ''.join(hit.contents)
        #See if string cotains the word resources
        if re.search("resources", str):

            #remove surrounding stuff
            str = str.replace(",", " ");
            str = str.replace("\"", " ");
            str = str.replace(":", " ");

            #Just take digits
            resources = [int(s) for s in str.split() if s.isdigit()]
            print('Resources:')
            print(resources)

    #Map Resource Fields + Levels

    currentfield = 1
    restype = ''

    for hit in soup.find_all('area'):

        if "Holzfäller" in hit.get('title'):
            restype = 'Holz'

        if "Getreidefarm" in hit.get('title'):
            restype = 'Getreide'

        if "Eisenmine" in hit.get('title'):
            restype = 'Eisen'

        if "Lehmgrube" in hit.get('title'):
            restype = 'Lehm'

        # New Subsoup for level
        subsoup = BeautifulSoup(hit.get('title'), 'lxml')

        # Cut to only relevant String and save as int in reslevel
        levelstr = subsoup.find(class_="level")
        reslevel = int(levelstr.string.split(" ")[1])

        # Set Update Scheme

        sql = """
        UPDATE fieldmap
        SET buildtype = ?, buildlevel = ?
        WHERE rowid = ?
        """

        # Execute Update
        Database.cursor.execute(sql, (restype, reslevel, currentfield))

        # Advance ID
        currentfield += 1

        # Stop after 18 Fields
        if currentfield == 19:
            break

    # Commit to Database
    Database.conn.commit()

def get_dorf2(session, server):
    # grab dorf2.php
    text = session.get(server + '/' + 'dorf2.php')
    # Into BS
    soup = BeautifulSoup(text.content, 'lxml')

    # Map Resource Fields + Levels
    for hit in soup.find_all('area'):
        # Get field ID
        field_id = int(hit.get('href').split('=')[1])

        # Get Name of building
        building_type = hit.get('alt').split(' ')[0]

        # Get Level of building
        # New Subsoup for level
        subsoup = BeautifulSoup(hit.get('alt'), 'lxml')
        # Cut to only relevant String
        building_level = subsoup.find(class_="level")

        if building_level is not None:
            building_level = int(building_level.string.split(" ")[1])

        # Set Update Scheme

        sql = """
        UPDATE fieldmap
        SET buildtype = ?, buildlevel = ?
        WHERE rowid = ?
        """

        # Execute Update
        Database.cursor.execute(sql, (building_type, building_level, field_id))

    # Commit to Database
    Database.conn.commit()

start = time.time()

server = set_server('ts3', 'de')
session = login('dorf1.php', server, 'Syntic', 'hacker1992')

Database.initialize_database()

# get_dorf1(session, server)
# get_dorf2(session, server)
print('Field ID Map:')
Database.print_database()
