# Search

## [Queries and filters](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-filter-context.html)

- __Filters__ ask a yes/no question of your data
- __Queries__ return data in terms of relevance

Use filters when you can - they are faster and cacheable. Basically, queries calculate relevance, whereas filters are used mostly for filtering structured data.

```bash
./curl -XGET 127.0.0.1:9200/movies/_search?pretty -d '
{
    "query": {                                              # query that contains
        "bool": {                                           # boolean experssion
            "must": {"term": {"title": "trek"}},            # must have "trek" in the title
            "filter": {"range": {"year": {"gte": 2010}}}    # must also have filter past the condition of the year being >= 2010
        }
    }
}'
```

### Some types of filters

- `term`: filter by exact values
    - `{"term": {"year": 2014}}`
- `terms`: match if any exact values in a list match
    - `{"terms": {"genre": ["Sci-Fi", "Adventure"]}}`
- `range`: find numbers or dates in a given range (gt, gte, lt, lte)
    - `{"range": {"year": {"gte": 2010}}}`
- `exists`: find documents where a field exists
    - `{"exists": {"field": "tags"}}`
- `missing`: find documents where a field is missing
    - `{"missing": {"field": "tags"}}`
- `bool`: combine filters with Boolean logic (`must`, `must_not`, `should`)

### Some types of queries

- `match_all`: returns all documents and is the default. Normally used with a filter.
    - `{"match_all": {}}`
- `match`: searches analyzed results, such as full text search
    - `{"match": {"title": "star"}`
- `multi_match`: run the same query on multiple fields
    - `{"multi_match": {"query": "star", "fields": ["title", "synopsis"]}}`
- `bool`: works like a bool filter, but results are scored by relevance


Examples of complex queries:
```bash
./curl -XGET 127.0.0.1:9200/movies/_search?pretty -d '
{
    "query": {
        "bool" :{
            "must": {"term": {"title": "trek"}},
            "filter": {"range": {"year": {"gte": 2010}}}
        }
    }
}'
# or this one for phrase matching in right order
./curl -XGET 127.0.0.1:9200/movies/_search?pretty -d '
{
    "query": {
        "match_phrase": {
            "title": "star wars"
        }
    }
}'
# or this one for phrase matching - order matters with some words being in between the terms, i.e. slop defines distance
./curl -XGET 127.0.0.1:9200/movies/_search?pretty -d '
{
    "query": {
        "match_phrase": {
            "title": {"query": "star beyond", "slop": 1}
        }
    }
}'
# or this one for phrase matching - results are sorted by relevance (docs that have the words closer together score higher)
./curl -XGET 127.0.0.1:9200/movies/_search?pretty -d '
{
    "query": {
        "match_phrase": {
            "title": {"query": "star beyond", "slop": 100}
        }
    }
}'
# or this one - complex query 1
./curl -XGET 127.0.0.1:9200/movies/_search?pretty -d '
{
    "query": {
        "bool": {
            "must": {"match": {"genre": "Sci-Fi"}},
            "must_not": {"match": {"title": "trek"}},
            "filter": {"range": {"year": {"gte": 2010, "lt": 2015}}}
        }
    }
}'
# or this one - complex query 2
./curl -XGET 127.0.0.1:9200/movies/_search?pretty -d '
{
    "sort": [{"title.raw": {"asc"}}],
    "query": {
        "bool": {
            "must": {"match": {"genre": "Sci-Fi"}},
            "filter": {"range": {"year": {"lt": 1960}}}
        }
    }
}'
# or this one - prefix matching
./curl -XGET 127.0.0.1:9200/movies/_search?pretty -d '
{
    "query": {
        "prefix": {
            "year": "201"   # supports wild-cards "1*"
        }
    }
}'
# or this one - prefix phrase matching
./curl -XGET 127.0.0.1:9200/movies/_search?pretty -d '
{
    "query": {
        "match_phrase_prefix": {
            "title": {
                "query": "star trek",
                "slop": 10              # supports wild-cards "1*"
            }
        }
    }
}'
```

## Pagination

`from` and `size` keywords are used for pagination and size:
```bash
./curl -XGET 127.0.0.1:9200/movies/_search?pretty -d '
{
    "from": 2,
    "size": 3,
    "query": {
        "match": {
            "title": "star beyond"
        }
    }
}'
```

## Sorting

`sort` keyword is used for sorting data:
```bash
./curl -XGET 127.0.0.1:9200/movies/_search?pretty -d '
{
    "sort" : [
        { "year" : "desc"}
    ],
    "query": {
        "match": {
            "title": "star beyond"
        }
    }
}'
```

## Fuzzy matches

Return documents that contain terms similar to the search term, as measured by a Levenshtein edit distance. `Fuzzinness` is the maximum edit distance allowed for matching.

```bash
./curl -XGET 127.0.0.1:9200/movies/_search?pretty -d '
{
    "query": {
        "fuzzy": {
            "title": {"value": "star beyond", "fuzziness": 2} # auto should generally be the preferred value
        }
    }
}'
```
