"""
This code is copied from ELVIS framework by Sergio Orgamas (MTG-UPF).
https://github.com/sergiooramas/elvis/blob/master/src/settings.py

ELVIS is a framework to homogenize and combine the output of different entity linking tools, 
using the level of agreement between different tools as a confidence score.
"""


import os

relative_path = os.getcwd()
PATH = relative_path[:relative_path.rfind("/")]
DBPEDIA_PATH = PATH+"/dbpedia/"
TEXTS_PATH = PATH+"/texts/"
DBPEDIA_SPOTLIGHT_ENDPOINT = "http://spotlight.sztaki.hu:2222/rest/annotate"
BABELFY_KEY = ""
TAGME_KEY = ""