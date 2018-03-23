#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:  Haidong Zhang
@Contact: haidong_zhang13@163.com
@License: (C) Copyright, 
@Time    : 2018/3/23 10:04
@Description: 
"""
from scipy.io import loadmat


class DataReader(object):
    def __init__(self):
        pass

    @staticmethod
    def load_matfile(filename, variable_name="network", is_directed=True):
        ''' Load data from .mat file.'''
        data = loadmat(filename)
        return data[variable_name]


    @staticmethod
    def load_edgelist(filename, is_directed=True):
        ''' Load data from .txt file. '''
        pass

    @staticmethod
    def load_walks(filename):
        ''' Load walks from filename. '''
        pass



if __name__ == '__main__':
    data = DataReader.load_matfile('../data/blogcatalog.mat', is_directed=False)
