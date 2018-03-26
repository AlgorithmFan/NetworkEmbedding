#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:  Haidong Zhang
@Contact: haidong_zhang13@163.com
@License: (C) Copyright, 
@Time    : 2018/3/25 10:28
@Description: 
"""
from collections import defaultdict


class MovieReader(object):
    '''
    Read movie data.
    '''
    def __init__(self):
        '''
        Initialization
        -----------------------------------------
        '''
        self.movies = defaultdict()
        self.ratings = defaultdict(defaultdict)

        self.actors = defaultdict()
        self.movie_actors = defaultdict(defaultdict)

        self.directors = defaultdict()
        self.movie_directors = defaultdict(defaultdict)

        self.genres = defaultdict()
        self.movie_genres = defaultdict(defaultdict)

    def load_movie_actors(self, filename=None):
        ''' Load movie actors. '''
        if filename is None:
            filename = '../data/movie/movie_actors.dat'

        with open(filename, 'r') as fp:
            fp.readline()
            for line in fp.readlines():
                temp = line.strip().split('\t')
                movie_id, actor_id, ranking = 'm_'+temp[0], 'a_'+temp[1], temp[3]
                self.movie_actors[movie_id][actor_id] = ranking
                self.actors[actor_id] = 1
        self.actors = {actor_id: index for index, actor_id in enumerate(self.actors.keys())}

    def load_movie_directors(self, filename=None):
        ''' Load Movie directors '''
        if filename is None:
            filename = '../data/movie/movie_directors.dat'

        with open(filename, 'r') as fp:
            fp.readline()
            for line in fp.readlines():
                temp = line.strip().split('\t')
                movie_id, director_id = 'm_'+temp[0], 'd_'+temp[1]
                self.movie_directors[movie_id][director_id] = 1.0
                self.directors[director_id] = 1
        self.directors = {director_id: index for index, director_id in enumerate(self.directors.keys())}

    def load_movie_genres(self, filename=None):
        ''' Load movie genres. '''
        if filename is None:
            filename = '../data/movie/movie_genres.dat'

        with open(filename, 'r') as fp:
            fp.readline()
            for line in fp.readlines():
                temp = line.strip().split('\t')
                movie_id, genre = 'm_'+temp[0], 'g_'+temp[1]
                self.movie_genres[movie_id][genre] = 1.0
                self.genres[genre] = 1
        self.genres = {genre: index for index, genre in enumerate(self.genres.keys())}

    def load_movies(self, filename=None):
        ''' Load movie data. '''
        if filename is None:
            filename = '../data/movie/movies.dat'

        with open(filename, 'r') as fp:
            fp.readline()
            for line in fp.readlines():
                temp = line.strip().split('\t')
                movie_id, movie_name = 'm_'+temp[0], temp[1]
                self.movies[movie_id] = movie_name

    def load_ratings(self, filename=None):
        ''' Load data from rating file. '''
        if filename is None:
            filename = '../data/movie/train_user_ratings.dat'

        with open(filename, 'r') as fp:
            fp.readline()
            for line in fp.readlines():
                temp = line.strip().split('\t')
                user_id, movie_id, rating = 'u_'+temp[0], 'm_'+temp[1], temp[2]
                self.ratings[user_id][movie_id] = rating

    def load_data(self, movie_actor_filename=None, movie_director_filename=None, movie_genre_filename=None,
                  movie_filename=None, movie_rating_filename=None):
        ''''''
        self.load_movie_actors(movie_actor_filename)
        self.load_movie_directors(movie_director_filename)
        self.load_movie_genres(movie_genre_filename)
        self.load_movies(movie_filename)
        self.load_ratings(movie_rating_filename)


if __name__ == '__main__':
    reader = MovieReader()
    reader.load_data()

    for user_id in reader.ratings:
        print '{}: {}'.format(user_id, len(reader.ratings[user_id]))
