from urllib import parse

import requests
import os
import bs4

username = input('moodle username: ')
password = input('password: ')

data = {'username': username,
        'password': password,
        'rememberusername': '1',
        'anchor': ''}
headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
login_url = 'http://219.219.120.72/login/index.php'
index_url = 'http://219.219.120.72/my/'

session = requests.Session()
session.post(login_url, data)

index_response_object = session.get(index_url)
index_soup = bs4.BeautifulSoup(index_response_object.text, features="html.parser")

courses_list = index_soup.select('[class="type_course depth_3 contains_branch"]')
courses_list_urls = list(map(lambda x: (x.a['href'], x.a['title']), courses_list))

for course in courses_list_urls:
    home = os.path.abspath('.')
    course_path = os.path.join(home, course[1])
    os.mkdir(course_path)
    course_soup = bs4.BeautifulSoup(session.get(course[0]).text, features='html.parser')
    doc_list = course_soup.select('[class="activity resource modtype_resource "]')
    doc_urls = list(map(lambda x: session.get(x.a['href']).url, doc_list))
    if doc_urls.__len__() != 0:
        for doc_url in doc_urls:
            print('downloading: ' + doc_url)
            temp = doc_url.split('/')
            filename = parse.unquote(temp[temp.__len__() - 1], encoding='utf8')
            with open(os.path.join(course_path, filename).encode('utf-8'), 'wb') as fd:
                fd.write(session.get(doc_url, stream=True).content)
