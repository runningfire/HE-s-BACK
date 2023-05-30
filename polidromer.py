# -*- coding: utf-8 -*-
"""
Created on Thu May 25 23:15:29 2023

@author: Alex
"""
import os
import requests


def words_getter() -> list:
    """

    Returns
    -------
    words :
    Обращается к словарю всех русских слов и получает список из них.

    """
    urlp1 = 'https://raw.githubusercontent.com/danakt/'
    urlp2 = 'russian-words/master/russian.txt'
    url = urlp1 + urlp2
    response = requests.get(url, timeout=10)
    text = response.content.decode('cp1251')
    words = text.split('\n')
    return words


def path_returner():
    path0 = input('Введите абсолютный путь, где файл')
    return path0

def finder_v2(words: list, path: str):
    """

    Parameters
    ----------
    words : list
        Считывает слово из файла находит слова,
        которые наоборот другие слова, и эти слова записывает в файл
        с дозаписью, так как обработка очень долгая,
        можно обрабатывать так в течение нескольких дней,
        функция будет дозаписывать.

    Returns
    -------
    None.

    """
    with open(path, 'a+', encoding='cp1251') as file:
        file.seek(0, os.SEEK_END)
        if file.tell() == 0:
            start_index = -1
            file.seek(0)
        else:
            file.seek(0)
            last_line = file.readlines()[-1]
            last_word = last_line.split('-')[0][:-1]
            start_index = words.index(last_word)
        for word in words[(start_index + 1):]:
            res = ''.join(reversed(word))
            if res in words:
                file.write(f"{word} - {res}\n")
                words.remove(word)
                try:
                    words.remove(res)
                except ValueError:
                    pass


if __name__ == '__main__':
    finder_v2(words_getter(), path_returner())
