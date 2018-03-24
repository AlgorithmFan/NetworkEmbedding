#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:  Haidong Zhang
@Contact: haidong_zhang13@163.com
@License: (C) Copyright, 
@Time    : 2018/3/23 10:16
@Description: 
"""


class DataWriter(object):
    def __init__(self):
        pass

    @staticmethod
    def write_walks(filename, walks):
        '''
        Write walks into filename.
        --------------------------------------
        Parameters:
            filename: walk file.
                type: str
            walks:
                type: list()
        '''
        with open(filename, 'w') as fp:
            for walk in walks:
                for node in walk:
                    fp.write('{}\t'.format(node))
                fp.write('\n')
