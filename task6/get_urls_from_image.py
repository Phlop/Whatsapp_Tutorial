#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Collect sources where images have previously appeared on, for a set of JSON
files describing a set of images.

@author: Hugo Sousa (hugosousa@dcc.ufmg.br)
'''


from argparse import ArgumentParser

import google_crawler as gc
import json
import os


# Add command line arguments.
parser = ArgumentParser()

parser.add_argument('image_url', type=str,
                    help='Path of the folder that contains the JSON files.')
parser.add_argument('pages', type=int,
                    help='Number of search result pages to go through.')
parser.add_argument('sleep_min', type=float,
                    help='Minimum number of seconds to sleep between \
                    requests.')
parser.add_argument('sleep_max', type=float,
                    help='Maximum number of seconds to sleep between \
                    requests.')

args = parser.parse_args()


def init():
    '''
        Initialize script.
    '''


def collect_sources():
    '''
        Collect sources where images have previously appeared on.
    '''
    
    
    if len(args.image_url) >= 5:
         google_url = gc.generate_search_url(args.image_url)
         print ('Getting URLs from %s :' %(google_url))
         sources = gc.get_sources(google_url, args.sleep_min, args.sleep_max, args.pages)
        
         print('Results found:')
         for s in sources:
             print (s)
    else:
        print ('Not valid url: %s' %(args.image_url))


def main():
    '''
        Main function.
    '''

    init()
    collect_sources()


main()
