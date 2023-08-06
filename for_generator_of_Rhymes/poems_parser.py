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
        href_list.append('url' + elem['href'])
    return href_list
        
def page_test(html):
    soup = BeautifulSoup(html, 'lxml')
    href_list = []
    for e in soup.find_all('div', class_='textlink nounline'):
        for elem in e.find_all('a'):
            href_list.append('url' + elem['href'])
    return href_list

def letters(inp):
    valids = []
    for character in inp:
        if (character.isalpha()) or (character.isspace()):
            valids.append(character)
    return (''.join(valids)).replace(u'\xa0', u'')

def get_poem(url):
    soup = BeautifulSoup(get_html(url), 'lxml')
    title = soup.find('title').text
    poem = ''
    for e in soup.find('div', class_='text'):
        poem = poem + e.text
    return poem, title, url

     



                

        