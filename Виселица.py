# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 07:54:20 2023

@author: home
"""

import codecs
import random
import time
from itertools import groupby


class GameLogic():

    def __init__(self, tries):
        self._tries = tries
        self.__end_game = False
        self.__end_play = False
        self.__tries0 = tries

    def cur_tries_counter(self):
        self._tries -= 1

    def hello_mess(self):
        print('Добро пожаловать в игру "Виселица"!')
        time.sleep(4)

    @property
    def end_play(self):
        return self.__end_play

    @property
    def end_game(self):
        return self.__end_game

    def filereader(self, path):
        """
        

        Parameters
        ----------
        path : str
            path to file with wordbank.

        Returns
        -------
        rndword : str
            Function read file with words generate list with them
            and choise random word from it and returns it.

        """
        
        word_list = []
        print('Генерирую слово...')
        time.sleep(3)
        with codecs.open(path, 'r', "utf-8") as file:
            for word in file:
                word = file.readline()
                word_list.append(word[:-2])
            rndword = random.choice(word_list)
            return rndword
        
    def getter_message(self):
        user_message = input(
            'Какая буква?\nЧтобы узнать сколько попыток осталось введите "1"\nЧтобы узнать какие буквы вы вводили нажмите "2"')
        return user_message

    def former_field(self, prev_state):
        spect_prev_state = '|'
        for i in range(len(prev_state)):
            spect_prev_state += prev_state[i] + ' |'
        print(f'Так выглядит поле сейчас:\n{spect_prev_state}')

    def game_state(self, rndword, prev_state, letter):
        current_word = ''
        spect_prev_state = '|'
        for i in range(len(rndword)):
            spect_prev_state += prev_state[i] + ' |'
            if rndword[i] == letter:
                current_word = current_word + rndword[i]
            else:
                current_word = current_word + prev_state[i]
        return current_word, (current_word) == (prev_state)

    def sorted_letters(self, letter, prev_state):
        state = ''
        prev_state += letter
        for element, _ in groupby(sorted(prev_state)):
            state += element + ' '
        return state

    def messager_tries(self):
        print(f'У вас осталось {self._tries} попыток')

    def end_playflag(self, rndword, current_word):
        if self._tries == 0:
            print(
                'К сожалению, вы проиграли, у вас закончились попытки.\nЭто было слово ' + rndword + '.')
            self.__end_play = True
        elif rndword == current_word:
            print('Поздравляю, вы отгадали слово. Это ' + rndword + '.')
            self.__end_play = True

    def end_gameflag(self):
        user_message = input(
            'Сгенерировать ещё слово? Отправьте любой символ. Не хотите играть, отправьте "0".')
        if user_message == '0':
            print('До новых встреч!')
            self.__end_game = True
        else:
            self.__end_play = False
            self._tries = self.__tries0

    @staticmethod
    def word_transformer(word):
        return '' + (len(word)) * ' '


if __name__ == '__main__': #C:\1\9. Движемся дальше\9.9 Домашнее задание Виселица\WordsStockRus.txt
    MAIN_PATH = input('Введите путь к файлу со словами')
    Game = GameLogic(5)
    while Game.end_game is False:
        Game.hello_mess()
        game_word = Game.filereader(MAIN_PATH)
        wd_for_player = Game.word_transformer(game_word)
        ENTERED_STATE = ''
        while Game.end_play is False:
            Game.former_field(wd_for_player)
            message = Game.getter_message()
            while (message.isalpha() is False) or (len(message) != 1):
                if message == '1':
                    Game.messager_tries()
                elif message == '2':
                    if ENTERED_STATE == '':
                        print('Вы пока ничего не вводили')
                    else:
                        print('Вы вводили ' + ENTERED_STATE)
                elif (message.isalpha()) and (len(message) == 1):
                    break
                else:
                    print('Некорректный ввод')
                time.sleep(3)
                message = Game.getter_message()
            Game_data = Game.game_state(game_word, wd_for_player, message)
            ENTERED_STATE = Game.sorted_letters(message, ENTERED_STATE)
            if Game_data[1]:
                Game.cur_tries_counter()
                print('Неправильно!')
            else:
                wd_for_player = Game_data[0]
                print('Угадано!')
            time.sleep(2)
            Game.end_playflag(game_word, wd_for_player)
        Game.end_gameflag()
