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
from scipy.sparse import issparse


class WalksCorpus(object):
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        with open(self.filename, 'r') as fp:
            for line in fp:
                yield line.strip().split('\t')


class DataReader(object):
    def __init__(self):
        pass

    @staticmethod
    def load_matfile(filename, variable_name="network"):
        ''' Load data from .mat file.'''
        data = loadmat(filename)
        r_data = list()

        if issparse(data[variable_name]):
            c_data = data[variable_name].tocoo()
            for i,j, w in zip(c_data.row, c_data.col, c_data.data):
                r_data.append((i, j, w))
        else:
            raise Exception("Dense matrices not yet supported.")
        return r_data

    @staticmethod
    def load_walks(filename):
        ''' Load data from walks. '''
        walks_corpus = WalksCorpus(filename)
        return walks_corpus

    @staticmethod
    def load_edgelist(filename, is_directed=True):
        ''' Load data from .txt file. '''
        pass





if __name__ == '__main__':
    data = DataReader.load_matfile('../data/blogcatalog.mat', is_directed=False)
