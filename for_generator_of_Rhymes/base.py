# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 23:34:33 2023

@author: Alex
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("postgresql+psycopg2://postgres:tal88og7nk@localhost:5432/poems")
Session = sessionmaker(bind=engine)


session = Session()

Base = declarative_base()