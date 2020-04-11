#!/bin/bash

mkdir -p /home/es_data
mkdir -p /home/mysql_database
chmod -R 777 /home/es_data
chmod -R 777 /home/mysql_database

mysql_config=$(cd `dirname $0`/mysql_config; pwd)
chmod -R 777 ${mysql_config}
echo "mysql config file:" ${mysql_config}
elk_config=$(cd `dirname $0`/elk_config; pwd)
chmod -R 777 ${elk_config}
echo "mysql config file:" ${elk_config}

docker stop kibana
docker rm kibana
docker stop elasticsearch
docker rm elasticsearch
docker stop qoslogstash
docker rm qoslogstash
docker stop server_nodes
docker rm server_nodes
docker stop indexer_mysql
docker rm indexer_mysql
docker network rm qos_network
docker network rm env_net

sudo systemctl restart docker
sudo docker pull 192.168.50.208:5000/ubuntuforjenkinsslave:v1

docker network create qos_network
docker run -d --name kibana --net qos_network -p 5601:5601 kibana:6.4.2
docker run -d --name elasticsearch --net qos_network -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -v /home/es_data:/usr/share/elasticsearch/data elasticsearch:6.4.2
docker run -d --name qoslogstash --rm --net qos_network -p 5000:5000/udp -v ${elk_config}:/config-dir logstash -f /config-dir/logstash.conf

docker network create --subnet=172.172.0.0/24 env_net
docker run -d -v /home:/home/workspace --net env_net --ip 172.172.0.10 --name server_nodes 192.168.50.208:5000/ubuntuforjenkinsslave:v2 /etc/init.d/ssh start -D
sudo docker run --net env_net --ip 172.172.0.11 -p 3306:3306 --name indexer_mysql -v /home/workspace/mysql_database:/var/lib/mysql -v ${mysql_config}:/etc/mysql/conf.d --privileged=true -e MYSQL_ROOT_PASSWORD=168168 -d mysql:5.7 --log-bin=/var/lib/mysql/mysql-bin --server-id=123456 --slow-query-log=1
