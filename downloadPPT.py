from urllib import parse

import sys
import requests
import os
import bs4


def url2filename(url):
    file = parse.unquote(url.split('/')[-1], encoding='utf8')
    if file.find("php") == -1:
        return file
    else:
        return None


def main(args):
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
    session.verify = False
    session.post(login_url, data=data, headers=headers)

    index_response_object = session.get(index_url)
    index_soup = bs4.BeautifulSoup(index_response_object.text, features="html.parser")

    courses_list = index_soup.select('[class="type_course depth_3 contains_branch"]')

    # 下载全部已选课程
    if len(args) == 1:
        courses_list_urls = list(map(lambda x: (x.a['href'], x.get_text()), courses_list))
    else:
        # courses_list_urls = [("http://219.219.120.72/course/view.php?id=106", "软件体系结构")]
        courses_list_urls = args[1:]

    for course in courses_list_urls:
        home = os.path.abspath('.')
        course_path = os.path.join(home, course[1])
        if not os.path.exists(course_path):
            os.mkdir(course_path)

        course_soup = bs4.BeautifulSoup(session.get(course[0]).text, features='html.parser')
        doc_list = course_soup.select('[class="activity resource modtype_resource "]')
        doc_urls = list(map(lambda x: session.get(x.a['href']).url, doc_list))

        for doc_url in doc_urls:
            filename = url2filename(doc_url)
            if filename is None:
                print(doc_url + " is not a file")
                continue
            print('downloading: ' + course[1] + '/' + filename)
            with open(os.path.join(course_path, filename), 'wb') as fd:
                fd.write(session.get(doc_url, stream=True).content)


if __name__ == '__main__':
    print(sys.argv)
    main(sys.argv)
