# Data normalization and relationships

Storage is very cheap these days, and one should not be optimizing based on minimizing your storage usage when you're talking about clusters of machines. It's more about: do I want the ablility to easily change that data, and do I have the capacity to deal with the increased traffic that normalization will bring along?

## Parent-child relationship

Let's model the parent-child relationship to the series to movies relation (like "Star Wars" series has following children as movies: "A New Hope", "Empire Strikes Back", "Return of the Jedi", "The Force Awakens", etc):

Let's begin with declaring a mapping for that relationship:

```bash
./curl -XPUT 127.0.0.1:9200/series -d '
{
    "mappings": {
        "properties": {
            "film_to_franchise": {
                "type": "join",
                "relations": {
                    "franchise": "film"
                }
            }
        }
    }
}'
```

The data for this index is at `./data/series.json`. Insert that data into relations index as following:

```bash
./curl -XPUT 127.0.0.1:9200/_bulk?pretty --data-binary @data/series.json
```

Query for doing a search to find all of the films in the Star Wars franchise:

```bash
./curl -XGET 127.0.0.1:9200/series/_search?pretty -d '
{
    "query": {
        "has_parent": {
            "parent_type": "franchise",
            "query": {
                "match": {
                    "title": "Star Wars"
                }
            }
        }
    }
}'
```

And query for doing a search to find specific franchise associated with the film:

```bash
./curl -XGET 127.0.0.1:9200/series/_search?pretty -d '
{
    "query": {
        "has_child": {
            "type": "film",
            "query": {
                "match": {
                    "title": "The Force Awakens"
                }
            }
        }
    }
}'
```

## [`flatened` data type](https://www.elastic.co/guide/en/elasticsearch/reference/7.16/flattened.html)

If we need to handle documents with many inner fields in JSON format, ES's performance can start to suffer due to **mapping explosion** (when an ES cluster crashes because of too many fields). This is because each subfield gets mapped to individual fields by default with dynamic mappings. To avoid this, ES provides `flattened` data type that maps as field as one flat data.

Example of mapping that might cause mapping explosion:

```bash
./curl -XPUT "http://127.0.0.1:9200/demo-flattened/_doc/1" -d '
{
    "message": "[5592:1:0309/123054.737712:ERROR:child_process_sandbox_support_impl_linux.cc(79)] FontService unique font name matching request did not receive a response.",
    "fileset": {
        "name": "syslog"
    },
    "process": {
        "name": "org.gnome.Shell.desktop",
        "pid": 3383
    },
    "@timestamp": "2020-03-09T18:00:54.000+05:30",
    "host": {
        "hostname": "bionic",
        "name": "bionic"
    }
}'
```

If we see the mapping, we can notice that ES has assigned types for each of the fields and subfields recursively:

```bash
curl -XGET "http://127.0.0.1:9200/demo-flattened/_mapping?pretty=true"
```

To avoid this dynamic mapping for every field, declare the host field as `flattened` and let's populate our index:

```bash
./curl -XDELETE "http://127.0.0.1:9200/demo-flattened"
./curl -XPUT "http://127.0.0.1:9200/demo-flattened"
./curl -XPUT "http://127.0.0.1:9200/demo-flattened/_mapping" -d '
{
    "properties": {
        "host": {
            "type": "flattened"
        }
    }
}'

./curl -XPUT "http://127.0.0.1:9200/demo-flattened/_doc/1" -d '
{
    "message": "[5592:1:0309/123054.737712:ERROR:child_process_sandbox_support_impl_linux.cc(79)] FontService unique font name matching request did not receive a response.",
    "fileset": {
        "name": "syslog"
    },
    "process": {
        "name": "org.gnome.Shell.desktop",
        "pid": 3383
    },
    "@timestamp": "2020-03-09T18:00:54.000+05:30",
    "host": {
        "hostname": "bionic",
        "name": "bionic",
        "osVersion": "Bionic Beaver",
        "osArchitecture":"x86_64"
    }
}'
```

And if we do search on the `host` field (that has `flattened` data type), it will return results based on whole phrase match:
```bash
./curl -XGET "http://127.0.0.1:9200/demo-flattened/_search?pretty=true" -d '
{
  "query": {
    "term": {
      "host": "Bionic Beaver"       
      # will return the results, since the field "host" has "Bionic Beaver" in its contents (full match)
    }
  }
}'
```

However `Bionic beaver` or `bionic beaver` won't return any results, since these are not matched directly with the data. The following one will work (nested field):
```bash
./curl -XGET "http://127.0.0.1:9200/demo-flattened/_search?pretty=true" -d '
{
    "query": {
        "term": {
            "host.osVersion": "Bionic Beaver"
            # but partial maps like "host.osVersion": "Beaver" will fail as fields are not analyzed
        }
    }
}'
```

In short, `flattened` data types provides nested queries for the data, however no analyzers are used so partial mappings are not supported, only exact matches.

Supported queries for flattened datatype:

- term, terms and terms_set
- prefix
- range (non numerical range operations)
- match and multi_match (we have to supply exact keywords)
- query_string and simple_query_string
- exists
