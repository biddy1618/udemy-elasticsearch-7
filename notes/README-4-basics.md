# Elasticsearch basics - Logical Concepts 

## Documents

Documents are the things you\re searching for. They can be more than text - any structured JSON data works. Every document has a unique ID, and a type.

## Index (Indices)

An index powers search into all documents within a collection of types. They contain inverted indices that let you search across everything within them at once, and mappings that define schemas for the data within.

So one can imaging that index is the table and documents are the rows within relational database (as an analogy). The scheme that defines tha data types in your documents also belongs to the index, you can only have one type of document within a single index and elastic search. __Think of your cluster as a database, indices as tables, and documents as rows in those tables__.

An index is actually what's called an inverted index and is basically the mechanism by which pretty much all search engines work. In simple words, the content of the document is represented in index, and search returns the index of the query input based on inverted indices, i.e. __an inverted index is what you're actually getting with a search index, where it's mapping things that you're searching for to the documents of those things live within, and of course it's not even quite that simple__.

The relevance of documents to query is measured through TF-IDF.

### Using indices

Three ways pf using an index in elastic search:

1. RESTful API

Any language that can talk to HTTP, can talk to an elastic search server through RESTful API.

2. Client API

3. Analytics Tools - like Kibana

## What's New In Elasticsearch 7

* The concept of document types is deprecated
* Elastic SQL is "production ready"
* Lots of changes to defaults (i.e., number of shards, replication)
* Lucene 8 under the hood
* Several X-Pack plugins now included with ES itself
* Bundled Java runtime
* Cross-cluster replication is "production ready"
* Index Lifecycle Management (ILM)
* High-level REST client in Java (HLRC)
* Lots of performance improvements
* Countless little breaking changes

## How Elasticsearch Scales

Documents are hashed to a particular shard -> Each shard may be on a different node in cluster -> Every shard is a self-contained Lucene index of its own.

Elasticsearche's main scaling trick is that an index is split into what we call shards, and every shard is basically a self-contained instance of lucene in and of itself. So the way ut works is once you actually talk to a given server on your cluster for elasticsearch, it figures out what document you're actually interested in, it can hash that to a oarticular shard ID, and it can redirect you to the appropriate shard in your cluster.

### Primary and Replica shards

This is how elastic search maintains resilience to failure. One big problem that you have when you have a cluster of computers is that those computers can fail sometimes and you need to deal with that. So for every cluster we will have number of __primary shards__ and __replicas__ (that is set while index definition). And whever one of the nodes fail for some reason, other nodes will come to help.

With this architecture `read` perform fast irregardles of the number of the nodes and shards, but `write` operation cost will increase correspondingly to the number of the shards.

NOTE: The number of shards and replicas are set up front and one needs to plan ahead and make sure that there are enough primary shards up front to handle any growth that might be reasonably expected. 


