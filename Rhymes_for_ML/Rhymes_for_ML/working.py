# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 15:18:26 2023

@author: Alex
"""

import parser_stihire


def letters(inp):
    valids = []
    for character in inp:
        if (character.isalpha()) or (character.isspace()):
            valids.append(character)
    return (''.join(valids)).replace(u'\xa0', u'')


def request_handler(start_url='https://stihi.ru/poems/selected.html'):
    start_html = parser_stihire.get_html(start_url)
    poems_links = []
    poems = []
    h_list = parser_stihire.page_test(start_html)
    for link in map(parser_stihire.get_html, h_list):
        poems_links.extend(parser_stihire.href_getterpage(link))
    for link in poems_links:
        try:
            poems.append(list(map(letters, parser_stihire.get_poem(link))))
        except:
            continue
    return poems


def word_catcher(poems):
    list_of_three_words = []
    for poem in poems:
        list_rhymes = []
        for verse in poem:
            words = verse.split(' ')
            stop_index = len(words) - 3
            del words[0:stop_index]
            if '' in words:
                words.remove('')
            list_rhymes.append(words)
        list_of_three_words.append(list_rhymes)
    return list_of_three_words


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
            
            
path = r'C:\Users\Alex\OneDrive\Python Scripts\Python Projects\Рифмы.txt'
txt_writer(path, word_catcher(request_handler()))    
            
                
                
            
    
    