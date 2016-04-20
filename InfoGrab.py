import requests
from bs4 import BeautifulSoup
import time

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

def get_page(server, page, session):
    text = session.get(server + '/' + page)



server = set_server('ts3', 'de')
session = login('dorf1.php', server, 'Synticus', 'travianpw')
text = session.get(server + '/' + 'dorf1.php')
print(text.content)