#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:  Haidong Zhang
@Contact: haidong_zhang13@163.com
@License: (C) Copyright, 
@Time    : 2018/3/26 11:31
@Description: 
"""
from collections import defaultdict
import codecs, json


class YelpReader(object):
    def __init__(self):
        '''
        Initialization
        -----------------------------------------
        '''
        self.users = defaultdict()
        self.items = defaultdict()
        self.train_data = list()
        self.test_data = list()

    def load_user(self):
        pass

    def load_business(self):
        pass

    def load_reviews(self):
        pass

    def load_reviews_with_time(self):
        pass

    def load_data(self):
        self.load_user()
        self.load_business()
        self.load_reviews()


if __name__ == '__main__':
    reader = YelpReader()
