#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:  Haidong Zhang
@Contact: haidong_zhang13@163.com
@License: (C) Copyright, 
@Time    : 2018/3/22 11:24
@Description: 
"""
from negative_sampling import NegativeSampling
from alias_sampling import AliasSampling
import random


class RandomWalk:
    def __init__(self, num_paths, path_length, alpha, sampler='negative_sampling'):
        self.num_paths = num_paths
        self.path_length = path_length
        self.alpha = alpha
        if sampler == 'negative_sampling' or sampler == 'NegativeSampling':
            self.sampler = NegativeSampling()
        elif sampler == 'alias_sampling' or sampler == 'AliasSampling':
            self.sampler = AliasSampling()
        else:
            raise Exception("Please choose a sampling method: NegativeSampling or AliasSampling.")

    def generate(self, graph):
        '''
        Generate random walks paths.
        -------------------------------------------------
        Parameters:
            graph:
        Returns:

        '''
        nodes = graph.keys()

        for index in range(self.num_paths):
            random.shuffle(nodes)
            for node in nodes:
                yield self.sampler.generate(graph, self.path_length, self.alpha, start=node)


    def generate_negative_samples(self):
        '''
        Generate negative samples.
        ----------------------------------------------------------
         Parameters:

        '''


