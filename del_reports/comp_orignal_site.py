from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.siam.org/meetings/sdm01/")
bsObj = BeautifulSoup(html)
for item in bsObj.findAll("li"):
	print(item.text)