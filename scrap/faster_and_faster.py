from selenium import webdriver
import codecs
import csv
import time
from selenium.common.exceptions import NoSuchElementException        
start = time.clock()
service_args=[]
service_args.append('--load-images=no')  ##关闭图片加载
service_args.append('--disk-cache=yes')  ##开启缓存
service_args.append('--ignore-ssl-errors=true') ##忽略https错误

driver = webdriver.PhantomJS("C:\ProgramData\Anaconda3\Scripts\phantomjs.exe",service_args=service_args)
s=time.clock()
driver.get("https://academic.microsoft.com/#/search?iq=%40ICDM%40&q=ICDM&filters=&from=0&sort=1")

driver.implicitly_wait(10)
# print ("aaaaaaa")
ss=time.clock()
# def check_exists_by_class_name(webelement,name):
#     try:
#         webelement.find_elements_by_class_name(name)
#     except NoSuchElementException:
#         return False
#     return True
print('open the phantomjs'+str(ss-s))
def find_lacks(ele_lists,ele_webs,d):
    titles = d.find_elements_by_class_name('paper-title')
    if(len(titles)>len(ele_lists)):
        flag=[]
        papers = d.find_elements_by_css_selector("paper-tile")



        for element in papers:
            flag.append(len(element.find_elements_by_class_name(ele_webs)))
            # if check_exists_by_class_name(element,ele_webs):
            #     flag.append('1')
            # else:
            #     flag.append('0')
            # print(len(element.find_elements_by_class_name(ele_webs)))

        for i in range(len(flag)):
            if flag[i] == 0:
                ele_lists.insert(i,'-')
        # print('the flag is:')
        # for i in flag:
        #     print(i)


        # print('find!')
    else:
        return
def split_empty(s):
    s1=[]
    for ele in s:
        if ele.text :
            s1.append(ele)
    return s1

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
    # print('abstract:'+str(len(abstracts)))
    abstracts = split_empty(abstracts)
    # print('abstract:'+str(len(abstracts)))
    times = d.find_elements_by_class_name('paper-year')
    venues = d.find_elements_by_class_name('paper-venue')
    aIDs = d.find_elements_by_class_name('authorIds')
    fields = d.find_elements_by_class_name('paper-fieldsOfStudy')
    # print('fields:'+str(len(fields)))
    fields =split_empty(fields)
    # print('fields:'+str(len(fields)))
    
   
    authors = [a.text for a in authors]
    abstracts = [a.text for a in abstracts]
    times = [a.text for a in times]
    venues = [a.text for a in venues]
    aIDs = [str(a.get_attribute('value')) for a in aIDs]
    fields = [a.text for a in fields]

    # for a in authors:
    #     a=a.text
    # for a in abstracts:
    #     a=a.text
    # for a in times:
    #     a=a.text
    # for a in venues:
    #     a=a.text
    # for a in aIDs:
    #     a=str(a.get_attribute("value"))
    # for a in fields:
    #     a=a.text

    s3=time.clock()
    
    # #if an article is lacked of one or two elements:
    # s1=time.clock()
    find_lacks(authors,'paper-authors',d)
    find_lacks(abstracts,'paper-abstract',d)
    find_lacks(times,'paper-year',d)
    find_lacks(venues,'paper-venue',d)
    find_lacks(aIDs,'paper-authorIds',d)
    find_lacks(fields,'paper-fieldsOfStudy',d)
    # find_lacks(authors,'paper-authors',d)   
    # s2=time.clock()
    # print('find_lacks time is'+ str(s2-s1)) 
    # print('open all folded tabs '+str(s2-s1))
    # print('find all '+str(s3-s2))
    # print('open the website '+str(ss-s))
    # print('after')
    # for i in range(len(fields)):
    #     print(fields[i])

    for title in titles:
        rows.append({'title': title.text,
                     'author': '',
                     'authorID':'',
                     'abstract':'',
                     'time': '',
                     'venue': '',
                     'field':''})


        
    for i in range(len(authors)):
        rows[i]['author'] = authors[i]
        rows[i]['authorID'] = aIDs[i]
        rows[i]['abstract'] = abstracts[i]
        rows[i]['time'] = times[i]
        rows[i]['venue'] = venues[i] 
        rows[i]['field'] = fields[i]
    
    # for i in rows:
    #     print(i.items())
    with codecs.open('./tests/acdatas_ICDM.csv',mode, encoding='utf-8') as f:
        f_csv = csv.DictWriter(f, headers)
        # f_csv.writeheader()
        f_csv.writerows(rows)

get_content(driver, 'w')
while True:
    try:
        start_jump=time.clock()
        link = driver.find_element_by_class_name('icon-angle-right')
    except NoSuchElementException:
        break
    link.click()
    end_jump=time.clock()
    print('time of jump'+str(end_jump-start_jump))
    get_content(driver,'a+')
    end_one_pass = time.clock()

    print('time of one pass'+str(end_one_pass-start_jump))

driver.close()
end = time.clock()

print(end-start)

