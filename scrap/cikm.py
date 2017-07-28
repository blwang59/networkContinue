from selenium import webdriver
import codecs
import csv
# import time
from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import WebDriverException
# start = time.clock()
import re

service_args = []
service_args.append('--load-images=no')  # 关闭图片加载
service_args.append('--disk-cache=yes')  # 开启缓存
service_args.append('--ignore-ssl-errors=true')  # 忽略https错误

driver = webdriver.PhantomJS(
    "C:\ProgramData\Anaconda3\Scripts\phantomjs.exe", service_args=service_args)
# driver = webdriver.PhantomJS()
# s=time.clock()
driver.get("https://academic.microsoft.com/#/search?iq=%40papers%20in%20conference%20CIKM%40&q=papers%20in%20conference%20CIKM&filters=&from=0&sort=1")
print('get CIKM')


driver.implicitly_wait(10)
# ss=time.clock()


def check_exists_by_class_name(webelement, name):
    try:
        webelement.find_elements_by_class_name(name)
    except NoSuchElementException:
        return False
    return True


def check_exists_by_partial_link_text(webelement, name):
    try:
        webelement.find_elements_by_partial_link_text(name)
    except NoSuchElementException:
        return False
    return True


def find_lacks(ele_lists, ele_webs, d):
    titles = d.find_elements_by_class_name('paper-title')
    if(len(titles) > len(ele_lists)):
        flag = []
        papers = d.find_elements_by_css_selector("paper-tile")

        for element in papers:
            flag.append(len(element.find_elements_by_class_name(ele_webs)))
            if check_exists_by_class_name(element, ele_webs) == False:
                flag.append(0)
            #     flag.append('1')
            # else:
            #     flag.append('0')
            # print(len(element.find_elements_by_class_name(ele_webs)))

        for i in range(len(flag)):
            if flag[i] == 0:
                ele_lists.insert(i, '-')
        # print('the flag is:')
        # for i in flag:
        #     print(i)

        # print('find!')
    else:
        return


def split_empty(s):
    s1 = []
    for ele in s:
        if ele.text:
            s1.append(ele)
    return s1


def get_content(d, mode):
    # s1=time.clock()

    # if check_exists_by_partial_link_text(d,' other'):

    button = d.find_elements_by_partial_link_text(' other')
    pattern = re.compile(r'.*\+\d+ others?')
    for b in button:
        if pattern.match(b.text):
            b.click()

    # s2=time.clock()

    headers = ['title', 'author', 'authorID',
               'abstract', 'time', 'venue', 'field']
    rows = []
    titles = d.find_elements_by_class_name('paper-title')

    authors = d.find_elements_by_class_name('paper-authors')
    
    authors_list = []
    for a in authors:
        author_string = ""
        every_author = a.find_elements_by_css_selector('li')
        for a1 in every_author:
            author_string += (a1.text+';')
        authors_list.append(author_string)


    abstracts = d.find_elements_by_class_name('paper-abstract')
    # print('abstract:'+str(len(abstracts)))
    abstracts = split_empty(abstracts)
    # print('abstract:'+str(len(abstracts)))
    times = d.find_elements_by_class_name('paper-year')
    venues = d.find_elements_by_class_name('paper-venue')
    aIDs = d.find_elements_by_class_name('authorIds')
    fields = d.find_elements_by_class_name('paper-fieldsOfStudy')
    # print('fields:'+str(len(fields)))
    fields = split_empty(fields)
    # print('fields:'+str(len(fields)))
    fields_list = []
    # print(len(fields))
    for f in fields:
        field_string = ""
        every_field = f.find_elements_by_css_selector('li')
        for f1 in every_field:
            field_string += (f1.text+';')
        fields_list.append(field_string)
        # print('1'+field_string)


    # authors = [a.text for a in authors]
    abstracts = [a.text for a in abstracts]
    times = [a.text for a in times]
    venues = [a.text for a in venues]
    aIDs = [str(a.get_attribute('value')) for a in aIDs]
    # fields = [a.text for a in fields]


    # s3=time.clock()

    # #if an article is lacked of one or two elements:
    # s1=time.clock()
    find_lacks(authors_list, 'paper-authors', d)
    find_lacks(abstracts, 'paper-abstract', d)
    find_lacks(times, 'paper-year', d)
    find_lacks(venues, 'paper-venue', d)
    find_lacks(aIDs, 'paper-authorIds', d)
    find_lacks(fields_list, 'paper-fieldsOfStudy', d)

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
                     'authorID': '',
                     'abstract': '',
                     'time': '',
                     'venue': '',
                     'field': ''})

    for i in range(len(authors)):
        rows[i]['author'] = authors_list[i]
        rows[i]['authorID'] = aIDs[i]
        rows[i]['abstract'] = abstracts[i]
        rows[i]['time'] = times[i]
        rows[i]['venue'] = venues[i]
        rows[i]['field'] = fields_list[i]

    # for i in rows:
    #     print(i.items())
    # with codecs.open('./tests/acdatas_ICDM.csv',mode, encoding='utf-8') as f:
    with codecs.open('./tests/acdatas_CIKM.csv', mode, encoding='utf-8') as f:
        f_csv = csv.DictWriter(f, headers)
        # f_csv.writeheader()
        f_csv.writerows(rows)

get_content(driver, 'w')

while True:
    try:
        link = driver.find_element_by_class_name('icon-angle-right')
    except NoSuchElementException:
        break
    link.click()
    get_content(driver, 'a+')

driver.close()
# end = time.clock()
# driver.quit()
# print(end-start)
