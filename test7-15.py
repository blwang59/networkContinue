from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import json
import csv
import codecs
import time
import re

start = time.clock()
driver = webdriver.PhantomJS()
# driver.get("https://academic.microsoft.com/#/search?iq=And(Ty%3D%270%27%2CComposite(CI.CIId%3D2326489083))&q=papers%20in\
# %20conference%20ICDM%202016&filters=&from=0&sort=1")
driver.get('https://academic.microsoft.com/#/search?iq=And(Ty%3D%270%27%2CComposite(C.CId%3D1183478919))&q=papers%20in\
%20conference%20icdm&filters=&from=0&sort=0')
# driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")
# try:
#     element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "loadedButton")))
# # element = WebDriverWait(element1, 10).until(EC.presence_of_element_located((By.ID, "loadedButton")))
# finally:

driver.implicitly_wait(10)


def get_content(d, mode):
    pattern = re.compile(r'\+ \d others')
    button = d.find_elements_by_partial_link_text('+ other')
    for b in button:
        b.click()

    headers = ['title', 'author', 'abstract', 'time', 'venue']
    rows = []
    titles = d.find_elements_by_class_name('paper-title')

    for title in titles:
        rows.append({'title': title.text,
                     'author': '',
                     'abstract': '',
                     'time': '',
                     'venue': ''})

    authors = d.find_elements_by_class_name('paper-authors')
    abstracts = d.find_elements_by_class_name('paper-abstract')
    times = d.find_elements_by_class_name('paper-year')
    venues = d.find_elements_by_class_name('paper-venue')


    for i in range(len(authors)):
        rows[i]['author'] = authors[i].text
        rows[i]['abstract'] = abstracts[i].text
        rows[i]['time'] = times[i].text
        rows[i]['venue'] = venues[i].text

    with codecs.open('acdatas.csv',mode, encoding='utf-8') as f:
        f_csv = csv.DictWriter(f, headers,)
        # f_csv.writeheader()
        f_csv.writerows(rows)

get_content(driver, 'w')
while True:
    try:
        link = driver.find_element_by_class_name('icon-angle-right')
    except NoSuchElementException:
        break
    link.click()
    get_content(driver,'a+')

driver.close()
end = time.clock()

print(end-start)
