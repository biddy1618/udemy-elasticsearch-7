# Concurrent CRUD operations

In order to avoid concurrency issues, use `retry_on_conflict` parameter in URL:
```bash
./curl -XPOST 127.0.0.1:9200/movies/_doc/109487/_update?retry_on_conflict=5 -d '
{
    "doc": {
        "title": "Interstellar Foo"
    }
}'
```

ES uses `_seq_no` and `_primary_term` options to deal with concurrency issues, one can see through `./curl -XGET 127.0.0.1:9200/_doc/109487?pretty`:
```bash
{
  "_index" : "movies",
  "_type" : "_doc",
  "_id" : "109487",
  "_version" : 1,
  "_seq_no" : 2,        # used to check concurrent updates
  "_primary_term" : 1,  # shard unique identifier
  "found" : true,
  "_source" : {
    "id" : "109487",
    "title" : "Interstellar",
    "year" : 2014,
    "genre" : [
      "Sci-Fi",
      "IMAX"
    ]
  }
}
```

Use following parameteres (`if_seq_no` and `if_primary_term`) for URL curl to update specific doc:
```bash
./curl -XPUT "127.0.0.1:9200/movies/_doc/109487?if_seq_no=2&if_primary_term=1" -d '
{
  "genres": ["IMAX", "Sci-Fi"],
  "title": "Interstellar Foo",
  "year": 2014
}`
```

# Analyzers

Sometimes text fields should be exact-match
- Use __keyword mapping__ instead of text

Search on analyzed text fields will return anything remotely relevant
- Depending on the analyzer, results will be case-sensitive, stemmed, stopwods removed, synonyms applied, etc.
- Searches with multiple terms need not match them all

## Search using `query`

The JSON syntax for quering using analyzer is as following:
```json
{
  "query": {
    "match": {                  # can be also "match_pharse", or other depending on the purpose
      "field": "match_phrase"   # set the field for searching, can be "genre" or "title"
    }
  }
}
```

More on the query details can be found [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-filter-context.html).

Using bash:
```bash
./curl -XGET 127.0.0.1:9200/movies/_search?pretty -d '
{
  "query": {
    "match": {
      "title": "star"
    }
  }
}`
```

So, basically the text query will be analyzed accordingly to the analyzer settings, like stemming, lemmatization, synonyms, partial matching for query with more than one word, etc. Depending on the index mapping, the analyzers will be different, so for text fields you want them to be more flexible and enable partial matching along with analyzer's transformations, whereas for categorical fields maybe you want them to match precisely. So, let's modify our index and make genre field `keywords` (more on the field data types [here](https://www.elastic.co/guide/en/elasticsearch/reference/7.16/mapping-types.html)). There are many of them like `binary`, `boolean`, `Keywords` (`keyword`, `constant_keyword`, `wildcard`), `Numbers` (`long`, `integer`, `short`, `byte`, etc), `text`, etc.
