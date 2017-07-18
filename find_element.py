from selenium import webdriver
import codecs
import csv
import time
from selenium.common.exceptions import NoSuchElementException        
start = time.clock()
print ("111111111111")
driver = webdriver.PhantomJS()
s=time.clock()
driver.get("https://academic.microsoft.com/#/search?iq=%40ICDM%40&q=ICDM&filters=&from=0&sort=1")

driver.implicitly_wait(10)
print ("aaaaaaa")
ss=time.clock()
def check_exists_by_class_name(webelement,name):
    try:
        webelement.find_elements_by_class_name(name)
    except NoSuchElementException:
        return False
    return True

def find_lacks(ele_lists,ele_webs,d):
    titles = d.find_elements_by_class_name('paper-title')
    if(len(titles)>len(ele_lists)):
        flag=[]
        papers = d.find_elements_by_css_selector("paper-tile")

        for element in papers:
            if check_exists_by_class_name(element,ele_webs):
                flag.append('1')
            else:
                flag.append('0')

        for i in range(len(flag)):
            if flag[i] == 0:
                ele_lists.insert(i,'-')
        for i in flag:
            print(i)


        print('find!')
    else:
        return
    
def get_content(d, mode):
    s1=time.clock()
    button = d.find_elements_by_partial_link_text(' other')
    for b in button:
        b.click()
    s2=time.clock()

    headers = ['title', 'author', 'authorID','abstract', 'time', 'venue','field']
    rows = []
    titles = d.find_elements_by_class_name('paper-title')

    authors = d.find_elements_by_class_name('paper-authors')
    abstracts = d.find_elements_by_class_name('paper-abstract')
    abstracts = abstracts[::2]
    times = d.find_elements_by_class_name('paper-year')
    venues = d.find_elements_by_class_name('paper-venue')
    aIDs = d.find_elements_by_class_name('authorIds')
    fields = d.find_elements_by_class_name('paper-fieldsOfStudy')
    fields = fields[::2]
    print ("bbbbbb")
    s3=time.clock()
    
    # #if an article is lacked of one or two elements:
    # s1=time.clock()
    find_lacks(authors,'paper-authors',d)
    find_lacks(abstracts,'paper-abstract-fieldsOfStudy',d)
    find_lacks(times,'paper-year',d)
    find_lacks(venues,'paper-venue',d)
    find_lacks(aIDs,'paper-authorIds',d)
    # find_lacks(authors,'paper-authors',d)   
    # s2=time.clock()
    # print('find_lacks time is'+ str(s2-s1)) 
    print('open all folded tabs '+str(s2-s1))
    print('find all '+str(s3-s2))
    print('open the website '+str(ss-s))


    for title in titles:
        rows.append({'title': title.text,
                     'author': '',
                     'authorID':'',
                     'abstract':'',
                     'time': '',
                     'venue': '',
                     'field':''})


        
    for i in range(len(authors)):
        rows[i]['author'] = authors[i].text
        rows[i]['authorID'] = str(aIDs[i].get_attribute("value"))
        rows[i]['abstract'] = abstracts[i].text
        rows[i]['time'] = times[i].text
        rows[i]['venue'] = venues[i].text 
        rows[i]['field'] = fields[i].text
    
    # for i in rows:
    #     print(i.items())
    with codecs.open('./tests/acdatas_page0_ICDM.csv',mode, encoding='utf-8') as f:
        f_csv = csv.DictWriter(f, headers)
        # f_csv.writeheader()
        f_csv.writerows(rows)

get_content(driver, 'w')
# while True:
#     try:
#         link = driver.find_element_by_class_name('icon-angle-right')
#     except NoSuchElementException:
#         break
#     link.click()
#     get_content(driver,'a+')

driver.close()
end = time.clock()

print(end-start)

