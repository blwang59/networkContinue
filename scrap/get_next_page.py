
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
driver = webdriver.Firefox()
driver.get('https://academic.microsoft.com/#/search?iq=And(Ty%3D%270%27%2CComposite(C.CId%3D1183478919))&q=papers%20in\
%20conference%20icdm&filters=&from=0&sort=0')
driver.implicitly_wait(10)
# driver.find_element_by_class_name('icon-angle-right').click()

page_number = 1
while page_number < 40:
    try:
        link = driver.find_element_by_class_name('icon-angle-right')
        print('find')
    except NoSuchElementException:
        print('not')
        break
    link.click()
    # print('1')
    # print(driver.current_url)
    page_number += 1
