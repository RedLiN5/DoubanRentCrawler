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
        cookie = {'Cookie':'ct=y; ap=1; ps=y; ll="108296"; __utmt=1; _ga=GA1.2.1545850150.1470297820; _gat_UA-7019765-1=1; ue="4372125@QQ.COM"; dbcl2="63247631:RTx25cp0Rdk"; ck=MIk5; push_noty_num=0; push_doumail_num=0; _pk_id.100001.8cb4=0c73410bb3c4761a.1470297777.4.1491123584.1491027175.; _pk_ses.100001.8cb4=*; __utma=30149280.1545850150.1470297820.1491027175.1491123542.4; __utmb=30149280.3.10.1491123542; __utmc=30149280; __utmz=30149280.1490949855.2.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=30149280.6324; _vwo_uuid_v2=15011FAE62D39D35F3E1381D306D622D|e5c4760540aeda3ad018f44b0537c92a'}
        cookie['Cookie'] = cookie['Cookie'] + '; bid=' \
                           + "".join(random.sample(string.ascii_letters + string.digits, 11))

        page = requests.get(url, headers=headers,
                            cookies=cookie,
                            timeout=(3.3, 5))
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


