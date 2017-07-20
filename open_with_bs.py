from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

try:
    html = urlopen("https://academic.microsoft.com/#/search?iq=%40ICDM%40&q=ICDM&filters=&from=0&sort=1")
except HTTPError as e:
    print(e)
else:
    bsObj = BeautifulSoup(html.read())
    
    

