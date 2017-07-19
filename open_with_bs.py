from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

try:
    html = urlopen('')
except HTTPError as e:
    print(e)
else:
    bsObj = BeautifulSoup(html.read())

