# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 23:49:40 2023

@author: Alex
"""

from poems_rhymes_model import PoemsData
from base import Session
from working import request_handler, word_catcher
import poems_parser

class NoNewData(Exception):
    pass



def from_sql_link_reader(session):
    data = session.query(PoemsData).all()
    return [record.link for record in data]

def sql_writer(author, poem, words, url, session):
    Data = PoemsData(author, poem, words, url)
    session.add(Data)


def main():
    site_urlist = request_handler()
    session = Session()
    sql_urlist = from_sql_link_reader(session)
    this_urlist = [url for url in site_urlist if url not in sql_urlist]
    if this_urlist:
        for elem in map(poems_parser.get_poem, this_urlist):
            author = elem[1]
            url = elem[2]
            poem, words = word_catcher(elem[0])
            sql_writer(author, poem, words, url, session)
    else:
        raise NoNewData("There's no new data from the webquery")
    session.commit()
    session.close()
    
main()
    
    
    