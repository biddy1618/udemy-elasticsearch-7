export CONTAINER_NAME=es

if [[ $(docker ps -a --format '{{.Names}}' | grep $CONTAINER_NAME) ]]; then
    echo "Found container under name $CONTAINER_NAME";
    if [ "`docker inspect -f {{.State.Running}} $CONTAINER_NAME`" == "false" ]; then
        echo "Container $CONTAINER_NAME state - not running";
        echo "Starting $CONTAINER_NAME";
        docker start es;
    fi
    echo "Container $CONTAINER_NAME started";
else
    echo "Starting container $CONTAINER_NAME in detached mode";
    docker run -d -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" --name $CONTAINER_NAME docker.elastic.co/elasticsearch/elasticsearch:7.16.3 > /dev/null 2>&1;
    
    read -p "Press enter to continue when container started";
    echo "Container started.";
    
    echo "Injecting data - data/shakes-mapping.json";
    curl -H "Content-Type: application/json" -XPUT '127.0.0.1:9200/shakespeare' --data-binary "@data/shakes-mapping.json" > /dev/null 2>&1;
    echo "Injecting data - data/shakespeare_7.0.json";
    curl -H "Content-Type: application/json" -XPOST '127.0.0.1:9200/shakespeare/_bulk' --data-binary "@data/shakespeare_7.0.json" > /dev/null 2>&1;
    
    echo "Injecting data - '{"mappings": {"properties": {"year": {"type": "date"}}}}'";
    curl -H "Content-Type: application/json" -XPUT 127.0.0.1:9200/movies --data-binary  "@data/movies-mapping.json" > /dev/null 2>&1;
    echo "Injecting data - data/movies.json";
    curl -H "Content-Type: application/json" -XPUT 127.0.0.1:9200/_bulk --data-binary "@data/movies.json" > /dev/null 2>&1;
fi;