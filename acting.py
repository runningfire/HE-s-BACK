# -*- coding: utf-8 -*-
"""
Created on Tue May 30 09:22:57 2023

@author: Alex
"""

from polidromer import path_returner
from polidromer_p2 import Handler

path_to_file = path_returner()


Handler = Handler(path_to_file)
Handler.selector(Handler.inputting(), Handler.reader())
