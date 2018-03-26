#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:  Haidong Zhang
@Contact: haidong_zhang13@163.com
@License: (C) Copyright, 
@Time    : 2017/8/8 11:00
@Description: 
"""
#!usr/bin/env python
#coding:utf-8

import datetime
import time


def get_month(timestamp):
    '''
    Get the month of timestamp, and transform it to timestamp
    -------------------------------------------------------------
    Parameters:
        timestamp: int
    Returns:
        monthStamp: the timetamp of this month.
    '''
    temp = datetime.datetime.fromtimestamp(timestamp)
    temp = datetime.datetime(year=temp.year, month=temp.month, day=1)
    month_stamp = time.mktime(temp.timetuple())
    return month_stamp

def get_week(timestamp):
    '''
    Get the week of timestamp, and transform it to timestamp
    '''
    weekth = int(time.strftime('%w', time.localtime(timestamp)))
    MondayStamp = timestamp - (weekth-1)*86400
    MondayStr = time.localtime(MondayStamp)
    return time.mktime(time.strptime(time.strftime('%Y-%m-%d', MondayStr), '%Y-%m-%d'))

def get_day(timestamp):
    '''
    Get the day of timestamp, and transform it to timestamp
    '''
    temp = datetime.datetime.fromtimestamp(timestamp)
    temp = datetime.datetime(year=temp.year, month=temp.month, day=temp.day)
    dayStamp = time.mktime(temp.timetuple())
    return dayStamp

def get_season(time_str):
    '''
    Get the timestamp of the season.
    ----------------------------------------------------------------------
    Parameters:
        timestamp: str, examples: 2009-1-2

    Returns:

    '''
    temp = time.strptime(time_str, '%Y-%m-%d')
    # season = 1
    if 1 <= temp.tm_mon <= 3:
        season = 0
    elif 4 <= temp.tm_mon <= 6:
        season = 1
    elif 7 <= temp.tm_mon <= 9:
        season = 2
    elif 10 <= temp.tm_mon <= 12:
        season = 3
    else:
        season = 0
        print 'Wrong: {}\t{}'.format(time_str, temp.tm_mon)

    return int('{}{}'.format(temp.tm_year, season))


def get_stamp(start_time, interval, flag):
    dayStr = time.localtime(start_time)
    year, month, day = dayStr.tm_year, dayStr.tm_mon, dayStr.tm_mday
    if flag == 'month':
        month += interval
        while month > 12:
            year += 1
            month -= 12
        end_time = time.mktime(time.strptime('%d-%d-%d' % (year, month, day), '%Y-%m-%d'))
    elif flag == 'week':
        end_time = start_time + 604800 * interval
    elif flag == 'day':
        end_time = start_time + 86400 * interval
    return end_time


if __name__ == '__main__':
    time_str = '2009-6-1'
    print get_season(time_str)
