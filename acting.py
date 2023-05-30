# -*- coding: utf-8 -*-
"""
Created on Tue May 30 09:22:57 2023

@author: Alex
"""

import sys
path0 = r'C:\Users\Alex\OneDrive\Python Scripts'
sys.path.insert(1, path0)
from polidromer import words_getter
from polidromer_p2 import *

Handler = Handler(path0)
Handler.selector(Handler.inputting(), Handler.reader())