# Installation methods and versioning

I will be using the last version of elastic search to be able to have all of the new features - i.e. 7.16.3.

CAVEAT: the course uses 7.0.0 version

## Methods of installation

### [Docker installation](https://www.elastic.co/guide/en/elasticsearch/reference/7.16/docker.html)

I will be using Docker container for installation.

```bash
docker pull docker pull docker.elastic.co/elasticsearch/elasticsearch:7.16.3
docker run -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" --name es docker.elastic.co/elasticsearch/elasticsearch:7.16.3
```

Check the browser at address - http://127.0.0.1:9200 or through bash `curl -XGET 127.0.0.1:9200`.

To connect to docker container, run the following:
```bash
docker exec -it es bash
```