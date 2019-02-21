import requests
from bs4 import BeautifulSoup


ses = requests.session()

req = requests.get('http://www.incois.gov.in/tsunami/Allevents.jsp')
page = BeautifulSoup(req.text, 'html-parser')
