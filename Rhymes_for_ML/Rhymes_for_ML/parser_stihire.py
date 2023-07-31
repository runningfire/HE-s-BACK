# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 18:30:47 2023

@author: Alex
"""

import requests as req
from bs4 import BeautifulSoup


def get_html(url):
    return req.get(url).text

def href_getterpage(html):
    soup = BeautifulSoup(html, 'lxml')
    href_list = []
    for elem in soup.find_all('a', class_='poemlink'):
        href_list.append('https://stihi.ru' + elem['href'])
    return href_list
        
def page_test(html):
    soup = BeautifulSoup(html, 'lxml')
    href_list = []
    for e in soup.find_all('div', class_='textlink nounline'):
        for elem in e.find_all('a'):
            href_list.append('https://stihi.ru' + elem['href'])
    return href_list

def get_poem(url):
    soup = BeautifulSoup(get_html(url), 'lxml')
    text_list = []
    for e in soup.find('div', class_='text'):
        strip = str(e).replace('<br/>', '').strip()
        if (len(strip) != 0) and (not strip.isspace()):
            text_list.append(strip)
    return text_list
        



                

        