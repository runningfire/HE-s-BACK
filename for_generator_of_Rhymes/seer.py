# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 02:18:28 2023

@author: Alex
"""

from base import Session
from poems_rhymes_model import PoemsData


text = input('Что хочешь посмотреть?')
session = Session()
data = session.query(PoemsData).all()
for record in data:
    print(getattr(record, text))
