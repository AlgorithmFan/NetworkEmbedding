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
        self.users = set()
        self.items = set()
        self.user_user = defaultdict(defaultdict)
        self.user_comp = defaultdict(defaultdict)
        self.item_city = defaultdict(defaultdict)
        self.item_cate = defaultdict(defaultdict)
        self.ratings = defaultdict(defaultdict)
        self.test_ratings = defaultdict(defaultdict)

    def load_users(self, filename=None):
        ''' Load users data. '''
        if filename is None:
            filename = '../data/yelp/users.json'

        with codecs.open(filename, mode='r', encoding='utf-8') as fp:
            while True:
                line = fp.readline().strip()
                if line == '':
                    break

                item = json.loads(line)
                if item['user_id'] in self.users:
                    for friend_id in item['friends']:
                        if friend_id in self.users:
                            self.user_user[item['user_id']][friend_id] = 1

    def load_items(self, filename=None):
        ''' Load items data. '''
        if filename is None:
            filename = '../data/yelp/business.json'

        with codecs.open(filename, mode='r', encoding='utf-8') as fp:
            while True:
                line = fp.readline().strip()
                if line == '':
                    break

                item = json.loads(line)
                if item['business_id'] in self.items:
                    for category in item['categories']:
                        self.item_cate[item['business_id']][category] = 1
                    self.item_city[item['business_id']][item['city']] = 1

    def load_ratings(self, filename=None):
        ''' Load reviews data. '''
        if filename is None:
            filename = '../data/yelp/split/train_0.json'

        with codecs.open(filename, mode='r', encoding='utf-8') as fp:
            while True:
                line = fp.readline().strip()
                if line == '':
                    break

                item = json.loads(line)
                self.users.add(item['user_id'])
                self.items.add(item['business_id'])
                self.ratings[item['user_id']][item['business_id']] = item['stars']

    def load_test_ratings(self, filename=None):
        ''' Load reviews data. '''
        if filename is None:
            filename = '../data/yelp/split/test_0.json'

        with codecs.open(filename, mode='r', encoding='utf-8') as fp:
            while True:
                line = fp.readline().strip()
                if line == '':
                    break

                item = json.loads(line)
                self.test_ratings[item['user_id']][item['business_id']] = item['stars']

    def load_ratings_with_time(self, filename=None):
        ''' Load reivews data with time. '''
        if filename is None:
            filename = '../data/yelp/reviews.json'

        with codecs.open(filename, mode='r') as fp:
            while True:
                line = fp.readline().strip()
                if line == '':
                    break

    def load_data(self, users_filename=None, items_filename=None, reviews_filename=None):
        self.load_ratings(reviews_filename)
        self.load_users(users_filename)
        self.load_items(items_filename)


if __name__ == '__main__':
    reader = YelpReader()
    reader.load_data()
