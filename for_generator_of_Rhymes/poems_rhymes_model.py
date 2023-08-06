# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 23:36:18 2023

@author: Alex
"""

from sqlalchemy import Column, String, Integer, Date, ARRAY, TEXT

from base import Base


class PoemsData(Base):
    __tablename__ = 'PoemsRhymes'
    
    
    id = Column(Integer, primary_key=True)
    author = Column(String(150), nullable=False)
    poem = Column(TEXT)
    link = Column(String(500))
    rhymes = Column(ARRAY(String))
    
    
    def __init__(self, author, poem, rhymes, link=None):
        if link is not None:
            self.link = link
        self.author = author
        self.poem = poem
        self.rhymes = rhymes
    
    
    