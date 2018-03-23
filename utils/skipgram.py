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
        logger = logging.getLogger(logger_name)
        self.vocabulary_counts = None
        kwargs["min_count"] = kwargs.get("min_count", 0)
        kwargs["workers"] = kwargs.get("workers", cpu_count())
        kwargs["size"] = kwargs.get("size", 128)
        kwargs["sentences"] = kwargs.get("sentences", None)
        kwargs["window"] = kwargs.get("window", 10)
        kwargs["sg"] = 1
        kwargs["hs"] = 1

        if vocabulary_counts != None:
            self.vocabulary_counts = vocabulary_counts
        Word2Vec.__init__(**kwargs)
