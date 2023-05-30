# -*- coding: utf-8 -*-
"""
Created on Tue May 30 07:19:06 2023

@author: Alex
"""
import sys
path0 = r'C:\Users\Alex\OneDrive\Python Scripts'
sys.path.insert(1, path0)
from polidromer import words_getter




class Handler:
    
    def __init__(self, path0):
        self.path = path0 + r'\Python Projects\Пары палиндромов.txt'
        
    
    def get_dict(self):
        print('Запрос к словарю русских слов...')
        self.words0 = words_getter()
        return self.words0
    
    
    def reader(self):
        print('Читаю файл...')
        with open(self.path, 'r', encoding='cp1251') as file:
            word_lines = file.readlines()
            for index, line in enumerate(word_lines):
                word_lines[index] = line.replace('\n', '')
            self._words = word_lines
        return self._words 
    
    
    def inputting(self):
        message1 = input('Введите первую букву')
        message2 = input('Введите последнюю букву')
        while (message1.isalpha() or message2.isalpha()) is False:
            message1 = input('Некорректный ввод, введите русскую букву')
            message2 = input('Некорректный ввод, введите русскую букву')
        message = (message1, message2)
        self._message = message
        return self._message
    
    
    def selector(self, message, words):
        select_condition = lambda w: (w[0] == message[0]) and (w[-1] == message[1])
        selected_pairs = []
        for pair in words:
            word = pair.split(' - ')[0]
            if select_condition(word):
                selected_pairs.append(pair)
        if any(selected_pairs):
            print('Вот такие я нашёл пары:', end='\n')
            for pair in selected_pairs:
                print(pair)
        else:
            print('Для такого сочетания пары не найдены')
        self._selected_pairs = selected_pairs
        return self._selected_pairs





         
        
        
           
           
   