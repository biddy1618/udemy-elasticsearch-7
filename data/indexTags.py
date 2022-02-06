import csv
from collections import deque
import elasticsearch
from elasticsearch import helpers

PATH_MOVIES = './data/ml-latest-small/movies.csv'
PATH_TAGS = './data/ml-latest-small/tags.csv'

def readMovies():
    csvfile = open(PATH_MOVIES, 'r')

    reader = csv.DictReader(csvfile)

    titleLookup = {}

    for movie in reader:
        titleLookup[movie['movieId']] = movie['title']

    return titleLookup

def readTags():
    csvfile = open(PATH_TAGS, 'r')

    titleLookup = readMovies()

    reader = csv.DictReader(csvfile)
    for line in reader:
        tag = {}
        tag['user_id'] = line['userId']
        tag['movie_id'] = line['movieId']
        tag['movie_title'] = titleLookup[line['movieId']]
        tag['tag'] = line['tag']
        tag['timestamp'] = line['timestamp']
        
        yield tag
    
es = elasticsearch.Elasticsearch()

es.indices.delete(index = 'tags', ignore = 404)
deque(helpers.parallel_bulk(es, readTags(), index = 'tags'), maxlen = 0)
es.indices.refresh()