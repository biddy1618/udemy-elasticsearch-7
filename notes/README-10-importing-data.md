# Data import

You can import from just about anything

- Stand-alone __scripts__ cab submit bulk documents via REST API
- __Logstash__ and __beats__ can stream data from logs, S3, databases, and more
- AWS systems can stream in data via __lambda__ or __kinesis firehose__
- __Kafka, spark__, and more have Elasticsearch integration add-ons

## Importing via script/json

Simple python ETL script
- Read in data from some distributed filesystem
- Transform in into JSON bulk inserts
- Submit via HTTP/REST to your elasticsearch cluster
```python
import csv
import re

csvfile = open('ml-latest-small/movies.csv', 'r')

reader = csv.DictReader( csvfile )
for movie in reader:
    print ('{"create": {"_index": "movies", "_id": "' , movie['movieId'], '"}}', sep = '')
    title = re.sub('\(.*\)$', '', re.sub('"','', movie['title']))
    year = movie['title'][-5:-1]
    if (not year.isdigit()):
        year = '2016'
    genres = movie['genres'].split('|')
    print ('{"id": "', movie['movieId'], '", "title": " ', title, '", "year": ', year, ', "genre": [', end = '', sep = '')
    for genre in genres[:-1]:
        print('"', genre, '",', end = '', sep = '')
    print('"', genres[-1], '"', end = '', sep = '')
    print (']}')
```

Populate __movies__ index with this data:
```bash
./curl -XDELETE 127.0.0.1:9200/movies
./curl -XPUT 127.0.0.1:9200/_bulk --data-binary @data/moremovies.json
```

## Client libraries

Free elsasticsearch client libraries are available for pretty much any language.
- __Java__ has a client maintained by elastic.co
- __Python__ has an elasticsearch package
- Elasticsearch-__ruby__
- Several choices for __scala__
- Elasticsearch.pm module for __perl__

You don't have to wrangle JSON:
```python
es = elasticsearch.Elasticsearch()

es.indices.delete(index = 'ratings', ignore = 404)
deque(helpers.parallel_bulk(es, readRatings(), index = 'ratings'), maxlen = 0)
es.indices.refresh()
```

## Python ES library

Install ES library in new conda environment:
```bash
conda create --name es python=3.8
conda activate es

# install elasticsearch 7.13.6
pip install elasticsearch==7.13.6
# or from requirements file
# pip install -r requirements.txt

# make sure that ES instance is running at localhost (127.0.0.1:9200)
python ./data/indexRatings.py
```

Check the injested data:
```bash
./curl 127.0.0.1:9200/ratings/_search?pretty
```

# Logstash

- Logstash parses, transforms, and filters data as it passes through
- It can derive stricture from unstructed data
- It can anonymize personal data or exclued it entirely
- It can do geo-location lookups
- It can scale across many nodes
- It guarantees at-least-once delivery
- It absorbs throughput from load spikes

See more [here](https://www.elastic.co/logstash/). For examples, see the course 