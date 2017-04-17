import requests
from bs4 import BeautifulSoup
from urllib import request
import os
from config import headers
from multiprocessing.dummy import Pool

final_list = []


def search_begin(name):
    url = 'http://www.ibtzz.com/?s=%s' % name
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    items = []
    alls = soup.find_all('a', class_='entry-thumb lazyload')
    for a in alls:
        new_url = a.get('href')
        title = a.get('title')
        print()
        new_item = {'url': new_url, 'title': title}
        items.append(new_item)
    return items


def get_detail_list(item):
    r = requests.get(item['url'], headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    div = soup.find('div', class_='entry-content lazyload')
    alls = div.find_all('a')
    for a in alls:
        href = a.get('href')
        if href:
            if href.find('dl_id') > 0:
                item['url'] = href
    final_list.append(item)


def get_serach_item(name):
    myitem = search_begin(name)
    pool = Pool()
    pool.map(get_detail_list, myitem)
    return final_list


