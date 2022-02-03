# Mapping and Indexing data

## Download toy dataset - MovieLens

```bash
wget http://media.sundog-soft.com/es/ml-latest-small.zip
unzip ml-latest-small.zip
rm ml-latest-small.zip
```

# Creating mappings

A mapping is a schema definition. Elasticsearch has reasonable defaults, but sometimes you need to customize them.

Example:
```bash
curl -H "Content-Type: application/json" -XPUT 127.0.0.1:9200/movies -d '
{
    "mappings": {
        "properties": {
            "year": {"type": "date"}
        }
    }
}'
```

## Get mapping definition


```bash
curl -H "Content-Type: application/json" -XGET 127.0.0.1:9200/movies/_mapping
```


## Common mappings

```bash
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


# More on mappings

A mapping essentially entails two parts:
- The process - defining how JSON documents will be stored
- The result - the actual metadata resulting from the definition process

## The mapping process

- Explicit mapping - fields and their types are predefined
- Dynamic mapping - fields and their types automatically defined ES

## Challenges

- Explicit mapping - mapping exceptions when there's a mismatch
- Dynamic mapping - may lead to mapping explosion

## Exceptions

When exceptions arise, one can use partially solve the issue by defining an ignore or malformed mapping parameter. This is not a dynamic parameter, so either it needs to be set when creating the index, or _close_ the index, change the setting, and _reopen_ the index.

Closing, changing the setting, and reopening index (more on the `microservice-logs` index in data folder):
```bash
./curl --request POST 'http://localhost:9200/microservice-logs/_close'
./curl --location --request PUT 'http://localhost:9200/microservice-logs/_settings' \
--data-raw '{
   "index.mapping.ignore_malformed": true
}'
./curl --request POST 'http://localhost:9200/microservice-logs/_open'
```

But this `index.mapping.ingore_malformed` parameter can't handle JSON objects as an input. For example, we have a field `message` with type `text` and if we post JSON data in field `message`, it is going to provoke an exception.

One more limitation to dynamic mappings is that once the mapping is defined, if we try to insert data with more nested field for JSON-like field, it will provoke exception as well.

On top of that, the default max number of fields for index is 1000, and if you try to define mapping with more than 1000 fields, ES will throw `illegal_argument_exception`. This setting can be change, however it might come with bigger complexity like performance degradations and high memory pressure,