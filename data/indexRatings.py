import csv
from collections import deque
import elasticsearch
from elasticsearch import helpers

PATH_MOVIES = './data/ml-latest-small/movies.csv'
PATH_RATINGS = './data/ml-latest-small/ratings.csv'

def readMovies():
    csvfile = open(PATH_MOVIES, 'r')

    reader = csv.DictReader(csvfile)

    titleLookup = {}

    for movie in reader:
        titleLookup[movie['movieId']] = movie['title']

    return titleLookup

def readRatings():
    csvfile = open(PATH_RATINGS, 'r')

    titleLookup = readMovies()

    reader = csv.DictReader(csvfile)
    for line in reader:
        rating = {}
        rating['user_id'] = int(line['userId'])
        rating['movie_id'] = int(line['movieId'])
        rating['title'] = titleLookup[line['movieId']]
        rating['rating'] = float(line['rating'])
        rating['timestamp'] = int(line['timestamp'])
        
        yield rating
    
es = elasticsearch.Elasticsearch()

es.indices.delete(index = 'ratings', ignore = 404)
deque(helpers.parallel_bulk(es, readRatings(), index = 'ratings'), maxlen = 0)
es.indices.refresh()
