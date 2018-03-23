#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:  Haidong Zhang
@Contact: haidong_zhang13@163.com
@License: (C) Copyright, 
@Time    : 2018/3/22 11:04
@Description: 
"""
from multiprocessing import cpu_count
import psutil
import os


class NetworkEmbedding(object):
    def __init__(self, filename, is_direct):
        self.filename = filename
        self.is_direct = is_direct

    def set_environment(self):
        # Set the parallel opt
        p = psutil.Process(os.getpid())
        try:
            p.set_cpu_affinity(list(range(cpu_count())))
        except AttributeError:
            try:
                p.cpu_affinity(list(range(cpu_count())))
            except AttributeError:
                pass


