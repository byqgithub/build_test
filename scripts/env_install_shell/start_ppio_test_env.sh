#!/bin/bash

function docker_restart(){
    date "+%Y-%m-%d_%H-%M-%S"
    config_path=$(cd `dirname $0`/mysql_config; pwd)
    echo "mysql config file:" ${config_path}

    mkdir -p /home/workspace/mysql_database
    chmod -R 777 /home/workspace/mysql_database
    chmod -R 777 ${config_path}

    sudo docker stop server_nodes
    sudo docker rm server_nodes
    sudo docker stop ppio_nodes
    sudo docker rm ppio_nodes
    sudo docker stop indexer_mysql
    sudo docker rm indexer_mysql
    sudo docker network rm env_net

    sudo systemctl restart docker
    sudo docker pull 192.168.50.208:5000/ppiosingleenv

    sudo docker network create --subnet=172.172.0.0/24 env_net
    sudo docker run -d --net env_net --ip 172.172.0.10 --name ppio_nodes -p 2222:22 -p 2379:2379 -p 8080:8080 -v /home/workspace/test_log:/tmp 192.168.50.208:5000/ppiosingleenv /etc/init.d/ssh start -D
    sudo docker run --net env_net --ip 172.172.0.11 -p 3306:3306 --name indexer_mysql -v /home/workspace/mysql_database:/var/lib/mysql -v ${config_path}:/etc/mysql/conf.d --privileged=true -e MYSQL_ROOT_PASSWORD=168168 -d mysql:5.7 --log-bin=/var/lib/mysql/mysql-bin --server-id=123456 --slow-query-log=1
}

docker ps | grep ppiosingleenv | grep -v grep
if [ $? -ne 0 ]
then
    echo "env recover"
    docker_restart
fi

if [ $1 = "restart" ]
then
    echo "env restart"
    docker_restart
fi
