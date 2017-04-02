# -*- coding: utf-8 -*-

import requests
import pandas as pd
import numpy as np
import bs4
from time import localtime, strftime
import random
import string

def start(urls=None, max_page=50, keywords=None):
    current_time = strftime("%Y-%m-%d_%H:%M:%S", localtime())
    if urls is None:
        raise ValueError('"urls" cannot be empty')

    if keywords is None:
        raise ValueError('"keywords" cannot be empty')

    if isinstance(urls, list):
        for url in urls:
            df, name = _crawler(url, max_page=max_page,
                                keywords=keywords)
            df.to_csv(name+current_time+'.csv',
                      index=False,
                      encoding='utf_8')
    elif isinstance(urls, str):
        df, name = _crawler(urls, max_page=max_page,
                            keywords=keywords)
        df.to_csv(name+current_time+'.csv',
                  index=False,
                  encoding='utf_8')
    print('Congratulations! Crawler is finished successfully!')

def _crawler(urlfront, max_page, keywords):
    columns = ['url', 'title', 'response_num']
    urls = []
    titles = []
    responses = []
    index = 0
    r = requests.Session()
    payload = {'form_email': '4372125@qq.com', 'form_password': 'andrew4372125'}
    p = r.post('https://www.douban.com/', data=payload)
    cookie_dict = p.cookies.get_dict()
    cookie_item = [name + '=' + cookie_dict[name] for name in cookie_dict if name != 'bid']
    cookie = {'Cookie': '; '.join(cookie_item)}
    url_temp = urlfront + 'discussion?start=' + str(0)
    page = requests.get(url_temp)
    soup = bs4.BeautifulSoup(page.content, 'lxml')
    text = soup.findAll('div', 'title')[0].text
    group_name = text.strip('\n')

    for page in range(max_page):
        page_index = page*25
        url = urlfront + 'discussion?start=' + str(page_index)
        headers = {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) "+
                                 "Gecko/20100101 Firefox/51.0"}
        cookie['Cookie'] = cookie['Cookie'] + '; bid=' \
                           + "".join(random.sample(string.ascii_letters + string.digits, 11))

        page = requests.get(url, headers=headers,
                            cookies=cookie,
                            timeout=(6.1, 5))
        soup = bs4.BeautifulSoup(page.content, 'lxml')
        items = soup.findAll('td', 'title')
        for item in items:
            target = item.find('a')
            href = target.attrs['href']
            response = item.find_parent().findAll('td')[2].text
            title = target.attrs['title']
            if any(s in title for s in keywords):
                urls.append(href)
                titles.append(title)
                responses.append(response)
                index += 1
    df = pd.DataFrame(data=np.array([urls, titles, responses]).T,
                                    columns=columns)
    return df, group_name


