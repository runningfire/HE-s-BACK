# -*- coding: utf-8 -*-
"""
Created on Tue May 30 07:19:06 2023

@author: Alex
"""
from polidromer import words_getter


class Handler:

    def __init__(self, path0):
        self.path = path0
        self.message = None
        self.words0 = None
        self.words = None
        self.selected_pairs = None

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
            self.words = word_lines
        return self.words

    def inputting(self):
        message1 = input('Введите первую букву')
        message2 = input('Введите последнюю букву')
        while (message1.isalpha() or message2.isalpha()) is False:
            message1 = input('Некорректный ввод, введите русскую букву')
            message2 = input('Некорректный ввод, введите русскую букву')
        message = (message1, message2)
        self.message = message
        return self.message

    def selector(self, message, words):
        def select_condition(input_word):
            return (input_word[0] == message[0]) and (input_word[-1] == message[1])
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
        self.selected_pairs = selected_pairs
        return self.selected_pairs
