# The Elastic Stack at high level

* Started off as scalable Lucene.
* Horizontally scalable search engine.
* Each "shard" is an inverted index of documents.
* But not just for full text search!
* Can handle structred data, and can aggregate data quickly.
* Often a faster solution than Hadoop/Spark/Flink/etc.

## Kibana overview

* Web UI for searching and visualizing.
* Complex aggregations, graphs, charts.
* Often used for log analysis.

## Logstach / Beats

* Ways to feed data into Elasticsearch.
* FileBeat can monitor log files, parse them and import into Elsaticsearch in near-real-time.
* Logstach also pushes data into Elasticsearch from many machines.
* Not just log files.

## X-Pack (paid service)

* Security
* Alerting
* Monitoring
* Reporting
* Machine Learning
* Graph Exploration