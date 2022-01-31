# Inserting single data

Inserting "Interstellar" movie into created index "movies" (ID of the movie is 109487 within MovieLens DB):
```
./curl -XPOST 127.0.0.1:9200/movies/_doc/109487 -d '
{
    "genre": ["IMAX", "Sci-Fi"],
    "title": "Interstellar",
    "year": 2014
}'
```

To get the all search results from our index:
```
./curl -XGET 127.0.0.1:9200/movies/_search?pretty
```

# Inserting bulk data

The insertion happens the following way:
```
./curl -XPUT 127.0.0.1:9200/_bulk -d '
{ "create" : { "_index" : "movies", "_id" : "135569" } }
{ "id": "135569", "title" : "Star Trek Beyond", "year":2016 , "genre":["Action", "Adventure", "Sci-Fi"] }
{ "create" : { "_index" : "movies", "_id" : "122886" } }
{ "id": "122886", "title" : "Star Wars: Episode VII - The Force Awakens", "year":2015 , "genre":["Action", "Adventure", "Fantasy", "Sci-Fi", "IMAX"] }
{ "create" : { "_index" : "movies", "_id" : "109487" } }
{ "id": "109487", "title" : "Interstellar", "year":2014 , "genre":["Sci-Fi", "IMAX"] }
{ "create" : { "_index" : "movies", "_id" : "58559" } }
{ "id": "58559", "title" : "Dark Knight, The", "year":2008 , "genre":["Action", "Crime", "Drama", "IMAX"] }
{ "create" : { "_index" : "movies", "_id" : "1924" } }
{ "id": "1924", "title" : "Plan 9 from Outer Space", "year":1959 , "genre":["Horror", "Sci-Fi"] }'
```

The reason why it is formatted this way is that Elasticsearch needs to distribute each documents into its own shard based on generated hash.

One can use file to insert the data as following:
```
./curl -XPUT 127.0.0.1:9200/_bulk?pretty --data-binary @data/movies.json
```

# Updating data

Every document has a `_version` field. Elasticsearch documents are immutable. When you update an existing document:
- a new documents is created with an incremented `_version`
- the old document is marked fir deletion

Update command (note that `-XPOST` method is used for updates):
```
./curl -XPOST 127.0.0.1:9200/movies/_doc/109487/_update -d '
{
    "doc": {
        "title": "Interstellar"
    }
}'
```
or one can insert whole document with updated fields:
```
./curl -XPUT 127.0.0.1:9200/movies/_doc/109487?pretty -d '
{
    "genres": ["IMAX", "Sci-Fi"],
    "title": "Interstellar Foo",
    "year": 2014
}'
```

To check:
```
./curl -XGET 127.0.0.1:9200/movies/_doc/109487?pretty
```

So, in summary, you can specify every field as a PUT command, or partial update as a POST command.

# Deleting data

To delete, use DELETE command with index and document specified to Elasticsearch host via HTTP call:
```
./curl -XDELETE 127.0.0.1:9200/movies/_doc/58559
```