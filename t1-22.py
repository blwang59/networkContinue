from selenium import webdriver
import json

from selenium.common.exceptions import NoSuchElementException
driver = webdriver.PhantomJS()
driver.get("https://academic.microsoft.com/#/search?iq=And(Ty%3D%270%27%2CComposite(CI.CIId%3D2326489083))&q=papers%20in\
%20conference%20ICDM%202016&filters=&from=0&sort=1")
import json
# driver.execute_script('''return new Promise(function(resolve, reject) {
#         var xhr = new XMLHttpRequest();
#         xhr.open(get, url, true);
#         xhr.responseType = 'json';
#         xhr.onload = function() {
#           var status = xhr.status;
#           if (status == 200) {
#             resolve(xhr.response);
#           } else {
#             reject(status);
#           }
#         };
#         xhr.send();
#       }); ''' )
# print (driver.find_element_by_tag_name('body').text)
# #
# print(driver.page_source)
page = 2
while True:
    try:
        link = driver.find_elements_by_link_text('page')
        print('find')
    except NoSuchElementException:
        print('not')
        break
    link.click()
    print('')
    print(driver.current_url)
    # page_number += 1