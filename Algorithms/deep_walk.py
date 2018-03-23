#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:  Haidong Zhang
@Contact: haidong_zhang13@163.com
@License: (C) Copyright, 
@Time    : 2018/3/22 11:05
@Description: 
"""
from network_embedding import NetworkEmbedding


class DeepWalk(NetworkEmbedding):
    def __init__(self, filename, is_direct):
        NetworkEmbedding.__init__(filename, is_direct)

