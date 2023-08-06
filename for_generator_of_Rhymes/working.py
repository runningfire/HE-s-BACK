# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 15:18:26 2023

@author: Alex
"""

import poems_parser



def request_handler(start_url='starturl'):
    start_html = poems_parser.get_html(start_url)
    poems_links = []
    h_list = poems_parser.page_test(start_html)
    for link in map(poems_parser.get_html, h_list):
        poems_links.extend(poems_parser.href_getterpage(link))
    return poems_links


def word_catcher(poem):
    poem = poems_parser.letters(poem)
    if poem[-1] != '\n':
        poem = poem + '\n'
    poem = poem.replace('  ', ' ')
    poem_list = poem.split('\n')
    words_list = []
    for verse in poem_list:
        if len(verse) > 0:
            if verse.startswith(' '):
                v = list(verse)
                del v[0]
                verse = ''.join(v)
            if verse.endswith(' '):
                v = list(verse)
                del v[-1]
                verse = ''.join(v)
            symbol_list = []
            for symbol in verse:
                if symbol.isalpha() or symbol.isspace():
                    symbol_list.append(symbol)
            new_verse = ''.join(symbol_list)
            words = new_verse.split(' ')[-3:]
            words_string = ''
            for word in words:
                words_string += word
                if word != words[-1]:
                    words_string += ' '
            words_list.append(words_string)
    return poem, words_list 


def txt_writer(path, list_of_words):
    with open(path, 'w', encoding='cp1251') as file:
        for poem in list_of_words:
            for verse in poem:
                for word in verse:
                    file.write(word)
                    if word != verse[-1]:
                        file.write(' ')
                    else:
                        file.write('\n')
            file.write('\n')


def txt_reader(path):
    with open(path, 'r', encoding='cp1251') as file:
        lines = file.readlines()
        all_wrds = []
        poem_wrds = []
        for line in lines:
            if line == '\n':
                all_wrds.append(poem_wrds)
                poem_wrds = []
            else:
                words = line.split(' ')
                words.remove('\n')
                poem_wrds.append(words)
        print(all_wrds)
            
            
   
            
    
    