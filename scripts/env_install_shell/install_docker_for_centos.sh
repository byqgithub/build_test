#!/bin/bash

sudo yum -y remove docker* \
                   docker-client* \
                   docker-client-latest* \
                   docker-common* \
                   docker-latest* \
                   docker-latest-logrotate* \
                   docker-logrotate* \
                   docker-selinux* \
                   docker-engine-selinux* \
                   docker-engine*

sudo yum install -y yum-utils device-mapper-persistent-data lvm2

sudo yum -y makecache fast

sudo yum -y install docker

echo "{\"insecure-registries\":[\"192.168.50.208:5000\"] }" > /etc/docker/daemon.json

sudo systemctl enable docker.service
sudo systemctl start docker

service crond restart

crontab env_cron

mkdir -p /home/workspace/test_log
