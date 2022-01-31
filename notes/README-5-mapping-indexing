# Mapping and Indexing data

## Download toy dataset - MovieLens

```
wget http://media.sundog-soft.com/es/ml-latest-small.zip
unzip ml-latest-small.zip
rm ml-latest-small.zip
```

# Creating mappings

A mapping is a schema definition. Elasticsearch has reasonable defaults, but sometimes you need to customize them.

Example:
```
curl -H "Content-Type: application/json" -XPUT 127.0.0.1:9200/movies -d '
{
    "mappings": {
        "properties": {
            "year": {"type": "date"}
        }
    }
}'
```

## Common mappings

```
{
    ... 
    "properties": {
        "user_id": {"type": "long"},            # string, byte, short, integer, long, float, double, boolean, date
        "genre": {"index": "not_analyzed"},     # do you want this field indexed for full-text search? analyzed/ not_analyzed/ no
        "description": {"analyzer": "english"}  # define your tokenizer and token filter. standard/ whitespace/ simple/ english etc.
        ...
    }
    ...
}
```

### More about the analyzers:
- Character filters
    - Remove HTML encoding, convert '&' to 'and'
- Tokenizer
    - Split strings on whitespace/ punctuation/ non-letters
- Token filter
    - Lowercasing, stemming, synonyms, stopwords (carefull with stopwords, like for "To be or not to be")

### Choices for analyzers
- Standard
    - Splits on word boundaries, removes punctuation, lowercases. Good choice if language is unknown
- Simple
    - Splits on anything that isn't a letter, and lowercase
- Whitespace
    - Splits on whitespace but doesn't lowercase
- Language (i.e. english)
    - Accounts for language-specific stopwords and stemming
