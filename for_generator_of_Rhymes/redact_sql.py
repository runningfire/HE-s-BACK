# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 17:15:13 2023

@author: Alex
"""

from base import engine
from sqlalchemy import Column, String

def add_column(engine, table_name, column):
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    engine.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table_name, column_name, column_type))


column = Column('link', String(100))
add_column(engine, 'PoemsRhymes', column)