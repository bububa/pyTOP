#!/usr/bin/env python
# encoding: utf-8
"""
test_crawler.py

Created by 徐 光硕 on 2011-11-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

from pyTOP.crawler import Crawler
from pprint import pprint

def main():
    crawler = Crawler()
    pprint(crawler.get_top_keywords())


if __name__ == '__main__':
    main()

