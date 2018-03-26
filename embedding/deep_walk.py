#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:  Haidong Zhang
@Contact: haidong_zhang13@163.com
@License: (C) Copyright, 
@Time    : 2018/3/22 11:05
@Description:
@Reference: https://github.com/phanein/deepwalk
"""
from network_embedding import NetworkEmbedding
from sampler.random_walk import RandomWalk
from utils.skipgram import Skipgram
from utils.data_writer import DataWriter


class DeepWalk(NetworkEmbedding):
    def __init__(self, graph, random_walk, is_directed):
        NetworkEmbedding.__init__(self, graph, random_walk, is_directed)

    def run(self, walk_filename, representation_size, window_size, model_filename):
        '''
        Training
        ----------------------------------------------
        Parameters:
            walk_filename: 随机游走的路径存储文件
                type: str
            representation_size: 表示的空间大小
                type: int
            window_size: 窗口大小
                type: int
            model_filename: 模型存储文件
                type: str
        '''
        num_walks = self.random_walk.num_paths * len(self.graph)
        print("Number of walks: {}".format(num_walks))

        data_size = num_walks * self.random_walk.path_length
        print("Data size (walks*length): {}".format(data_size))

        print("Walking....")
        walks = self.random_walk.generate(self.graph)
        DataWriter.write_walks(walk_filename, walks)

        walks_corpus = DataReader.load_walks(walk_filename)
        model = Skipgram(sentences=walks_corpus, size=representation_size, window=window_size, min_count=0, trim_rule=None, workers=self.workers)
        # model.wv.save_word2vec_format(walk_filename[:8], )
        model.save(model_filename)
        print 'Terminal.'


if __name__ == '__main__':
    from utils.data_reader import DataReader
    from utils.graph import Graph
    data = DataReader.load_matfile('../data/blogcatalog.mat')

    is_directed = False
    graph = Graph(data, is_directed)
    random_walk = RandomWalk(num_paths=5, path_length=5, alpha=0.0)

    algorithm = DeepWalk(graph, random_walk, is_directed)
    algorithm.run(walk_filename='../data/deepwalk.walks', representation_size=100, window_size=5, model_filename='../data/deepwalk.model')
