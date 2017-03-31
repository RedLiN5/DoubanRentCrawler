# -*- coding: utf-8 -*-

import requests
from lxml import etree
import re
import datetime
import pandas as pd
import numpy as np
import glob
import os
import sys
import bs4

def start(urls=None, max_page=50, keywords=None):
    if urls is None:
        raise ValueError('"urls" cannot be empty')

    if keywords is None:
        raise ValueError('"keywords" cannot be empty')

    if isinstance(urls, type):
        pass
    elif isinstance(urls, str):
        pass

def _crawler(urlfront, max_page, keywords):
    columns = ['url', 'title', 'response']
    df = pd.DataFrame(columns=columns)
    index = 0
    url_temp = urlfront + str(0)
    page = requests.get(url_temp)
    soup = bs4.BeautifulSoup(page.content, 'lxml')
    text = soup.findAll('div', 'title')[0].text
    group_name = text.strip('\n')

    for page in range(max_page):
        page_index = page*25
        url = urlfront + str(page_index)
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.content, 'lxml')
        items = soup.findAll('td', 'title')
        for item in items:
            target = item.find('a')
            href = target.attrs['href']
            response = item.find_parent().findAll('td')[2].text
            title = target.attrs['title']
            if any(s in title for s in keywords):
                df.ix[index,:] = href, title, response
                index += 1
    return df, group_name

