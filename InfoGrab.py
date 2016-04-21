import requests
from bs4 import BeautifulSoup
import time
import re

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

    for hit in soup.find_all('area'):

        if "Holzfäller" in hit.get('title'):
            print('ID', currentfield, 'Holz')
            currentfield += 1

        if "Getreidefarm" in hit.get('title'):
            print('ID', currentfield, 'Getreide')
            currentfield += 1

        if "Eisenmine" in hit.get('title'):
            print('ID', currentfield, 'Eisen')
            currentfield += 1

        if "Lehmgrube" in hit.get('title'):
            print('ID', currentfield, 'Lehm')
            currentfield += 1

        #New Subsoup for level
        subsoup = BeautifulSoup(hit.get('title'), 'lxml')
        #Cut to only relevant String
        result = subsoup.find(class_="level")
        print(result.string)
        if currentfield == 19:
            break


server = set_server('ts3', 'de')
session = login('dorf1.php', server, 'Synticus', 'travianpw')
get_dorf1(session, server)