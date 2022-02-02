# Injesting demo - Shakespear data

Download Shakespear data:
```bash
# index mapping
wget http://media.sundog-soft.com/es7/shakes-mapping.json

# data in json format
wget http://media.sundog-soft.com/es7/shakespeare_7.0.json
```

Injesting the data:
```bash
curl -H "Content-Type: application/json" -XPUT 127.0.0.1:9200/shakespeare --data-binary @shakes-mapping.json
curl -H "Content-Type: application/json" -XPOST '127.0.0.1:9200/shakespeare/_bulk' --data-binary @shakespeare_7.0.json
```

Test the injested data:
```bash
curl -H "Content-Type: application/json" -XGET '127.0.0.1:9200/shakespeare/_search?pretty' -d '
{
    "query": {
        "match_phrase": {
            "text_entry": "to be or not to be"
        }
    }
}'
```

or use the query file:
```bash
curl -H "Content-Type: application/json" -XGET '127.0.0.1:9200/shakespeare/_search?pretty' -d @query.json
```