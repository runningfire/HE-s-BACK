# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 02:04:00 2023

@author: Alex
"""

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