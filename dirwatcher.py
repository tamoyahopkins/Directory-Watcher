#!/usr/bin/env python

import logging, os


__author__ = 'tamoyahopkins'

# logging config
startup_banner = ''
shutdown_banner = ''
logger = ''

# program
current_dict = {}
state = {}


def watch_dir():
    pass


def search_dict(dict, text):
    '''Searches dict files for text.  Stores last line searched.  Returns updated dict.'''
    if dict:
        print('dict is NOT empty')
    else:
        print('dict IS empty')


search_dict(current_dict, 'hello')