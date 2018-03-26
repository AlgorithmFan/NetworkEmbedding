#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:  Haidong Zhang
@Contact: haidong_zhang13@163.com
@License: (C) Copyright, 
@Time    : 2018/3/26 17:15
@Description: 
"""

import json
import codecs
from utils.get_time import get_season
from utils.config_reader import ConfigReader
import matplotlib.pyplot as plt


class Dataset(object):

    @staticmethod
    def read_reviews(reviews_filename, users_filename, businesses_filename):
        '''
        Get the users and businesses from reviews_filename, and save them into filenames, respectively.
        -----------------------------------------------------------------------------------------------
        Parameters:
            reviews_filename: reviews filename
                type: str
            users_filename: users filename, saving users
                type: str
            businesses_filename: businesses filename, saving businesses
                type: str
        '''
        reviews_num = 0
        users, businesses = dict(), dict()
        with codecs.open(reviews_filename, mode='r', encoding='utf-8') as fp:
            while True:
                line = fp.readline().strip()
                if line == '':
                    break

                reviews_num += 1
                item = json.loads(line)
                users.setdefault(item['user_id'], 0)
                users[item['user_id']] += 1
                businesses.setdefault(item['business_id'], 0)
                businesses[item['business_id']] += 1

        with codecs.open(users_filename, mode='w', encoding='utf-8') as fp:
            fp.write(json.dumps(users))

        with codecs.open(businesses_filename, mode='w', encoding='utf-8') as fp:
            fp.write(json.dumps(businesses))

        print 'The number of users is {}.'.format(len(users))
        print 'The number of businesses is {}.'.format(len(businesses))
        print 'The number of reviews is {}.'.format(reviews_num)

    @staticmethod
    def read_reviews_over_time(reviews_filename, users_filename, businesses_filename):
        '''
        Get the users and businesses changing over time from reviews_filename, and save them into filenames, respectively.
        -----------------------------------------------------------------------------------------------
        Parameters:
            reviews_filename: reviews filename
                type: str
            users_filename: users filename, saving users changing over time
                type: str
            businesses_filename: businesses filename, saving businesses changing over time
                type: str
        '''
        reviews_num = 0
        season_users, season_businesses = dict(), dict()
        with codecs.open(reviews_filename, mode='r', encoding='utf-8') as fp:
            while True:
                line = fp.readline().strip()
                if line == '':
                    break

                reviews_num += 1
                item = json.loads(line)
                season = get_season(item['date'])

                # add users
                season_users.setdefault(season, set())
                season_users[season].add(item['user_id'])

                # add businesses
                season_businesses.setdefault(season, set())
                season_businesses[season].add(item['business_id'])

        with codecs.open(users_filename, mode='w', encoding='utf-8') as fp:
            for season in season_users.keys():
                season_users[season] = list(season_users[season])
            json.dump(season_users, fp)
            # fp.write(json.dumps(season_users))

        with codecs.open(businesses_filename, mode='w', encoding='utf-8') as fp:
            for season in season_businesses.keys():
                season_businesses[season] = list(season_businesses[season])
            json.dump(season_businesses, fp)
            # fp.write(json.dumps(season_businesses))

        print 'The number of reviews is {}.'.format(reviews_num)
        seasons = season_users.keys()
        seasons.sort()
        for season in seasons:
            print 'Season {}: {}-users, {}-businesses'.format(season, len(season_users[season]), len(season_businesses[season]))

    @staticmethod
    def get_filtered_users(filename, threshold):
        '''
        Get the filtered users who has more than threshold reviews,
        or get the filtered businesses which has more than threshold reviews.
        --------------------------------------------------------------------------------
        Parameters:
            filename: the user filename or the business filename
        Returns:
            filtered_users: the users set
        '''
        with codecs.open(filename, mode='r', encoding='utf-8') as fp:
            users = json.load(fp)

        filtered_users = set()
        for user_id, num in users.items():
            if num > threshold:
                filtered_users.add(user_id)
        return filtered_users

    @staticmethod
    def filter_reviews_users_businesses(reviews_filename, users, businesses, filtered_reviews_filename):
        '''
        Filter the reviews according to whether the user is in users and the business is in businesses
        -----------------------------------------------------------------------------------------------
        Parameters:
            reviews_filename: str
            users: set()
            businesses: set()
            filtered_reviews_filename: str
        '''
        with codecs.open(reviews_filename, mode='r', encoding='utf-8') as fp:
            with codecs.open(filtered_reviews_filename, mode='w', encoding='utf-8') as filtered_fp:
                while True:
                    line = fp.readline()
                    if line == '':
                        break

                    item = json.loads(line)
                    if item['user_id'] in users and item['business_id'] in businesses:
                        filtered_fp.write(line)

    @staticmethod
    def filter_reviews_time_range(reviews_filename, time_start, time_num, filtered_reviews_filename):
        '''
        Filter the reviews from time_start to time_start+time_num
        -----------------------------------------------------------------------------------------------
        Parameters:
            reviews_filename: str
            users: set()
            businesses: set()
            filtered_reviews_filename: str
        '''
        # time_num -= 1
        time_1 = time_start%10 + time_num%4
        time_2 = int(time_start/10)%10 + int(time_1/4) + int(time_num/4)
        time_end = int(time_start/100)*100 + time_2*10 + time_1%4

        with codecs.open(reviews_filename, mode='r', encoding='utf-8') as fp:
            with codecs.open(filtered_reviews_filename, mode='w', encoding='utf-8') as filtered_fp:
                while True:
                    line = fp.readline()
                    if line == '':
                        break

                    item = json.loads(line)
                    season = get_season(item['date'])
                    if time_start <= season < time_end:
                        filtered_fp.write(line)

    @staticmethod
    def filter_users(filename, users, filtered_filename):
        '''
        Filter the users according to whether the user_id in users.
        --------------------------------------------------------------------------
        Parameters:
            filename: str
            users: set()
            filtered_filename: str
        '''
        with codecs.open(filename, mode='r', encoding='utf-8') as fp:
            with codecs.open(filtered_filename, mode='w', encoding='utf-8') as filtered_fp:
                while True:
                    line = fp.readline()
                    if line == '':
                        break

                    item = json.loads(line)
                    if item['user_id'] not in users:
                        continue

                    friends = list()
                    for user_id in item['friends']:
                        if user_id in users:
                            friends.append(user_id)
                    item['friends'] = friends
                    filtered_fp.write(json.dumps(item) + '\n')

    @staticmethod
    def filter_businesses(filename, businesses, filtered_filename):
        '''
        Filter the businesses
        ---------------------------------------------------------------------
        Parameters:
            filename: str
             businesses: set()
             filtered_filename: str
        '''
        with codecs.open(filename, mode='r', encoding='utf-8') as fp:
            with codecs.open(filtered_filename, mode='w', encoding='utf-8') as filtered_fp:
                while True:
                    line = fp.readline()
                    if line == '':
                        break

                    item = json.loads(line)
                    if item['business_id'] not in businesses:
                        continue

                    filtered_fp.write(line)

    @staticmethod
    def count_businesses(filename):
        '''
        Count the number of businesses, the number of categories, the number of stars, the number of states, the number of cities.
        ------------------------------------------------------------------------------
        Parameters:
            filename: the filename of business.
        '''
        categories, stars, states, cities = set(), set(), set(), set()
        businesses_num, categories_num, stars_num, states_num, cities_num = 0, 0, 0, 0, 0

        with codecs.open(filename, mode='r', encoding='utf-8') as fp:
            for line in fp.readlines():
                item = json.loads(line)
                categories.update(set(item['categories']))
                stars.add(item['stars'])
                states.add(item['state'])
                cities.add(item['city'])

                businesses_num += 1
                categories_num += len(item['categories'])
                stars_num += 1
                states_num += 1
                cities_num += 1

        print 'The number of businesses is {}.'.format(businesses_num)
        print 'The number of categories is {}'.format(len(categories))
        print 'The number of business-category relations is {}.'.format(categories_num)
        print 'The number of stars is {}.'.format(len(stars))
        print 'The number of business-star relations is {}.'.format(stars_num)
        print 'The number of states is {}.'.format(len(states))
        print 'The number of business-state relations is {}'.format(states_num)
        print 'The number of cities is {}.'.format(len(cities))
        print 'The number of business-city relations is {}.'.format(cities_num)

    @staticmethod
    def count_users(filename):
        '''
        Count the number of users, the number of friends
        -------------------------------------------------------------------------
        Parameters:
            filename: the user filename
        '''
        users_num, friends_num = 0, 0
        with codecs.open(filename, mode='r', encoding='utf-8') as fp:
            for line in fp.readlines():
                item = json.loads(line)
                friends_num += len(item['friends'])
                users_num += 1

        print 'The number of users is {}.'.format(users_num)
        print 'The number of friends is {}.'.format(friends_num)

    @staticmethod
    def count_reviews(filename):
        '''
        Count the number of reviews, the number of business-reviews.
        ----------------------------------------------------------------------------
        Parameters:
            filename: the review filename.
        '''
        stars = set()
        reviews_num, business_reviews_num = 0, 0
        with codecs.open(filename, mode='r', encoding='utf-8') as fp:
            while True:
                line = fp.readline().strip()
                if line == '':
                    break
                item = json.loads(line)
                stars.add(item['stars'])
                reviews_num += 1
                business_reviews_num += 1

        print 'The number of reviews is {}.'.format(reviews_num)
        print 'The number of stars is {}.'.format(len(stars))
        print 'The number of business-review relations is {}.'.format(business_reviews_num)

    @staticmethod
    def count_reviews_over_time(filename):
        '''
        Count the number of reviews changing over time
        ------------------------------------------------------------------------------------
        Parameters:
            filename: the review filename
        '''
        time_reviews_num = dict()
        time_users, time_businesses = dict(), dict()
        with codecs.open(filename, mode='r', encoding='utf-8') as fp:
            while True:
                line = fp.readline()
                if line == '':
                    break
                item = json.loads(line.strip())

                season = get_season(item['date'])

                time_users.setdefault(season, set())
                time_users[season].add(item['user_id'])

                time_businesses.setdefault(season, set())
                time_businesses[season].add(item['business_id'])

                time_reviews_num.setdefault(season, 0)
                time_reviews_num[season] += 1

        time_reviews_num = sorted(time_reviews_num.items(), key=lambda x:x[0])
        for time, num in time_reviews_num:
            print 'Season {}: {}-reviews, {}-users, {}-businesses'.format(time, num, len(time_users[time]), len(time_businesses[time]))

    @staticmethod
    def count_time_users(filename, time_start, time_num):
        '''
        Count common users from time_start to time_start+time_num
        ---------------------------------------------------------------------
        Parameters:
            filename: str
            time_start: int
            time_num: int
        Returns:

        '''
        with codecs.open(filename, encoding='utf-8') as fp:
            time_users = json.load(fp)
        time_keys = time_users.keys()
        time_keys.sort()
        start_index = time_keys.index(str(time_start))
        users = set(time_users[time_keys[start_index+time_num]])
        for i in range(time_num):
            users &= set(time_users[time_keys[start_index+time_num-i]])
        print 'The number of users is {}.'.format(len(users))
        return users

    @staticmethod
    def split(filename, split_path, time_start, time_num):
        '''
        Split the data into train and test according to the time intervals
        '''
        # Ge the end time season
        time_1 = time_start%10 + time_num%4
        time_2 = int(time_start/10)%10 + int(time_1/4) + int(time_num/4)
        time_end = int(time_start/100)*100 + time_2*10 + time_1%4

        time_reviews_filenames = dict()
        with codecs.open(filename, mode='r', encoding='utf-8') as fp:
            while True:
                line = fp.readline()
                if line == '':
                    break

                item = json.loads(line.strip())
                season = get_season(item['date'])
                if not (time_start <= season < time_end):
                    continue

                filename = split_path + '{}.json'.format(season)
                if filename not in time_reviews_filenames:
                    time_reviews_filenames[filename] = codecs.open(filename, encoding='utf-8', mode='w')
                time_reviews_filenames[filename].write(line)

        for filename in time_reviews_filenames:
            time_reviews_filenames[filename].close()


if __name__ == '__main__':
    import os
    config_reader = ConfigReader(config_filename='../config/yelp.ini')
    filtered_path = config_reader['path', 'filtered_path', 'string']
    if not os.path.exists(filtered_path):
        os.makedirs(filtered_path)

    if 0:
        print '-' * 50 + 'Filtering' + '-'*50
        print '*' * 50
        print 'Count user-reviews number and business-reviews number.'
        reviews_filename = config_reader['path', 'reviews_filename', 'string']
        users_num_filename = filtered_path + config_reader['path', 'users_num_filename', 'string']
        businesses_num_filename = filtered_path + config_reader['path', 'businesses_num_filename', 'string']
        Dataset.read_reviews(reviews_filename, users_num_filename, businesses_num_filename)

        print '*' * 50
        print 'Count season-users and season-businesses over time.'
        season_users_filename = filtered_path + config_reader['path', 'season_users_filename', 'string']
        season_businesses_filename = filtered_path + config_reader['path', 'season_businesses_filename', 'string']
        Dataset.read_reviews_over_time(reviews_filename, season_users_filename, season_businesses_filename)

        print '*' * 50
        print 'Filter reviews according to common users and common businesses over time.'
        season_start = config_reader['path', 'season_start', 'int'] # 2010 spring and 28 seasons
        seasons_num = config_reader['path', 'seasons_num', 'int']
        filtered_reviews_filename_time = filtered_path + config_reader['path', 'filtered_reviews_filename_time', 'string'].format(season_start, seasons_num)
        Dataset.filter_reviews_time_range(reviews_filename, season_start, seasons_num, filtered_reviews_filename_time)

        print '*' * 50
        print 'Filter users num'
        users_num_threshold = config_reader['path', 'users_num_threshold', 'int']
        filtered_users_set = Dataset.get_filtered_users(users_num_filename, threshold=users_num_threshold)
        print 'The number of users more than {}-reviews is {}.'.format(users_num_threshold, len(filtered_users_set))

        print '*' * 50
        print 'Filter businesses num.'
        businesses_num_threshold = config_reader['path', 'businesses_num_threshold', 'int']
        filtered_businesses_set = Dataset.get_filtered_users(businesses_num_filename, threshold=businesses_num_threshold)
        print 'The number of businesses more than {}-reviews is {}.'.format(businesses_num_threshold, len(filtered_businesses_set))

        print '*' * 50
        print 'Filter reviews according to filtered_users_set and filtered_businesses_set.'
        filtered_reviews_filename_ub = filtered_path + config_reader['path', 'filtered_reviews_filename_ub', 'string']
        Dataset.filter_reviews_users_businesses(reviews_filename, filtered_users_set, filtered_businesses_set, filtered_reviews_filename_ub)

        print '*' * 50
        print 'Filter users attribute.'
        users_filename = config_reader['path', 'users_filename', 'string']
        filtered_users_filename = filtered_path + config_reader['path', 'filtered_users_filename', 'string']
        Dataset.filter_users(users_filename, filtered_users_set, filtered_users_filename)

        print '*' * 50
        print 'Filter businesses attribute.'
        businesses_filename = config_reader['path', 'businesses_filename', 'string']
        filtered_businesses_filename = filtered_path + config_reader['path', 'filtered_businesses_filename', 'string']
        Dataset.filter_businesses(businesses_filename, filtered_businesses_set, filtered_businesses_filename)

        print '*' * 50
        print 'Split the data according to the time slices.'
        split_filename = filtered_path + config_reader['path', 'filtered_reviews_filename_ub', 'string']
        split_path = config_reader['path', 'split_path', 'string']
        Dataset.split(split_filename, split_path, season_start, seasons_num)

    print '-'*50 + 'Counting' + '-'*50
    print '*' * 50
    print 'Counting users...'
    filtered_users_filename = filtered_path + config_reader['path', 'filtered_users_filename', 'string']
    Dataset.count_users(filtered_users_filename)

    print '*' * 50
    print 'Counting businesses...'
    filtered_businesses_filename = filtered_path + config_reader['path', 'filtered_businesses_filename', 'string']
    Dataset.count_businesses(filtered_businesses_filename)

    print '*' * 50
    print 'Counting reviews over time ....'
    season_start = config_reader['path', 'season_start', 'int']  # 2010 spring and 28 seasons
    seasons_num = config_reader['path', 'seasons_num', 'int']
    filtered_reviews_filename_time = filtered_path + config_reader[
        'path', 'filtered_reviews_filename_time', 'string'].format(season_start, seasons_num)
    Dataset.count_reviews_over_time(filtered_reviews_filename_time)
    Dataset.count_reviews(filtered_reviews_filename_time)

    print '*' * 50
    print 'Counting reviews of filtered_users and filtered_businesses over time...'
    filtered_reviews_filename_ub = filtered_path + config_reader['path', 'filtered_reviews_filename_ub', 'string']
    Dataset.count_reviews_over_time(filtered_reviews_filename_ub)
    Dataset.count_reviews(filtered_reviews_filename_ub)

    print '*' * 50
    print 'Counting reviews of users over time ...'
    season_users_filename = filtered_path + config_reader['path', 'season_users_filename', 'string']
    Dataset.count_time_users(season_users_filename, season_start, 16)

    print '*' * 50
    print 'Counting reviews of businesses over time.'
    season_businesses_filename = filtered_path + config_reader['path', 'season_businesses_filename', 'string']
    Dataset.count_time_users(season_businesses_filename, season_start, 16)
