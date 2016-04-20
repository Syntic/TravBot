import requests
from bs4 import BeautifulSoup
import time

import os

# def scan():
#
#     print(os.getcwd())
#
#     with open('dorf1.php', 'r', encoding='UTF-8') as f:
#         data = f.read()
#
#     soup = BeautifulSoup(data, "lxml")
#     print(soup.prettify())
#
#
#
#
# scan()

def login(page, server, domain, username, password):

    # Generate new URL
    url = 'http://' + server + '.travian.' + domain + '/' + page

    # Open session & add user agent
    s = requests.session()
    s.headers.update({'user-agent': 'Mozilla/5.0'})

    # Set Login Data
    login_data = dict(name=username, password=password, s1='Einloggen', login=time.time())
    # Send login data to login page
    s.post(url, data=login_data)
    # get page after login
    r = s.get(url)

login('dorf1.php', 'ts3', 'de', 'Synticus', 'travianpw')