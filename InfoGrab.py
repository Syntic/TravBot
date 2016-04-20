import requests
from bs4 import BeautifulSoup
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

def login(page, server, domain):

    # Generate new URL
    # url = 'http://' + server + '.travian.' + domain + '/' + page
    # print(url)

    # Open session & add user agent
    s = requests.session()
    s.headers.update({'user-agent': 'Mozilla/5.0'})

    # Set Login Data
    login_data = dict(name='Synticus', password='travianpw', s1='Einloggen')

    # Send login data to login page
    l = s.post('http://ts3.travian.de/login.php', data=login_data)
    print(l.status_code)
    print(l.content)

    postcont = BeautifulSoup(l.content, "lxml")
    print(postcont.prettify())

    # print content that should be available off a page after login
    r = s.get('http://ts3.travian.de/dorf1.php')

    # print(r.status_code)
    # print('----------------------------------------')
    # print(r.content)
    #
    # soup = BeautifulSoup(r.content, "lxml")
    # print(soup.prettify())

login('dorf2.php', 'ts3', 'de')
