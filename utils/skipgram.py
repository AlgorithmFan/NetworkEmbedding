#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:  Haidong Zhang
@Contact: haidong_zhang13@163.com
@License: (C) Copyright, 
@Time    : 2018/3/22 11:39
@Description: 
"""
from collections import Counter, Mapping
from concurrent.futures import ProcessPoolExecutor
import logging
from multiprocessing import cpu_count
from six import string_types

from gensim.models import Word2Vec
from gensim.models.word2vec import Vocab


class Skipgram(Word2Vec):
    """ A subclass to allow more customization of the Word2Vec internals. """
    def __init__(self, vocabulary_counts=None, logger_name="", **kwargs):
        '''
        Initialization
        -----------------------------------------------------
        Parameters:
            min_count: 对字典做阶段，少于min_count次数的单词会被丢弃，默认值为5.
            size： 隐藏层的单元数，默认值为100，推荐值为几十到几百
            workers： 控制训练并行， 默认是1，worker参数只有安装了Cython后才有效，没有的话，只能使用单核
        '''
        logger = logging.getLogger(logger_name)
        self.vocabulary_counts = None
        kwargs["min_count"] = kwargs.get("min_count", 5)
        kwargs["workers"] = kwargs.get("workers", cpu_count())
        kwargs["size"] = kwargs.get("size", 128)
        kwargs["sentences"] = kwargs.get("sentences", None)
        kwargs["window"] = kwargs.get("window", 10)
        kwargs["sg"] = 1
        kwargs["hs"] = 1

        if vocabulary_counts != None:
            self.vocabulary_counts = vocabulary_counts
        Word2Vec.__init__(self, **kwargs)
