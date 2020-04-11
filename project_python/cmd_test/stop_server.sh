#!/bin/bash
go_path="$1"
script_path=$(cd `dirname $0`; pwd)
echo "go_path: " $1
echo "current path: " $script_path
echo "Stop user and miner"
cd $go_path/src/github.com/PPIO/go-ppio/
echo $(pwd)
for pid in `screen -ls | grep -e ppiox.user -e ppiox.miner | cut -d '.' -f 1`; do
	  kill -9 $pid
done
screen -wipe
screen ls


echo "Stop ppio server"
cd $go_path/src/github.com/PPIO/go-ppio/
for pid in `screen -ls | grep ppiox | cut -d '.' -f 1`; do
	  kill -9 $pid
done
screen -wipe
screen ls


echo "Stop gppio"
cd $go_path/src/github.com/PPIO/gppio/
for pid in `screen -ls | grep gppio | cut -d '.' -f 1`; do
  kill -9 $pid
done
screen -wipe


echo "Clear gppio DB"
cd $go_path/src/github.com/PPIO/gppio/
./clearDB.sh


echo "Clear redis"
redis-cli -h 127.0.0.1 -p 6379 -a "" flushall

echo "Clear mysql"
mysql -h 172.172.0.11 -uroot -p168168 < ${script_path}/delete_mysql_data.sql

echo "Clear user miner data"
cd $go_path/src/github.com/PPIO/go-ppio/
rm -rf ${script_path}/config/user*/*.db
rm -rf ${script_path}/config/user*/*.log
rm -rf ${script_path}/config/user*/storage

if [ $2 = "miner_clean" ]
then
    echo "clean miner"
    rm -rf ${script_path}/config/miner*/*.db
    rm -rf ${script_path}/config/miner*/*.log
    rm -rf ${script_path}/config/miner*/miner-*
fi
