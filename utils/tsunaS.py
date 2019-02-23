import requests
from bs4 import BeautifulSoup
import csv

ses = requests.session()

req = requests.get('http://www.incois.gov.in/tsunami/Allevents.jsp')
page = BeautifulSoup(req.text, 'html.parser')

tb = page.find('tbody')

with open('drew.csv', 'w+') as f:
    cr  = csv.writer(f)

    for tr in tb.find_all('tr'):
        td_list = [ td.text for td in tr.find_all('td')]
        print(td_list)
        if len(td_list) < 4:
            print('Skip')
            continue
        cr.writerow(td_list)
