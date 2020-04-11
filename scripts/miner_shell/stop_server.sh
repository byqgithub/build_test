#!/bin/bash

echo "Stop user and miner"
for pid in `screen -ls | grep -e ppiox.user -e ppiox.miner | cut -d '.' -f 1`; do
      kill -9 $pid
done
screen -wipe
screen ls


#echo "Start ppio server"
#for pid in `screen -ls | grep ppiox | cut -d '.' -f 1`; do
#      kill -9 $pid
#done
#screen -wipe
#screen ls


#echo "Stop gppio"
#for pid in `screen -ls | grep gppio | cut -d '.' -f 1`; do
#      kill -9 $pid
#done
#screen -wipe
#screen ls


#echo "Clear gppio DB"
#cd $GOPATH/src/github.com/PPIO/ppio-chain/
#./clearDB.sh


#echo "Clear redis"
#redis-cli -h 127.0.0.1 -p 6379 -a "" flushall

#echo "export mysql"
#mkdir -p /tmp/test_log/mysql_data
#cd /tmp/test_log/mysql_data
#mysqldump -h 172.172.0.11 -u root -p168168 ppio > ./mysql_data_$(date "+%Y-%m-%d_%H-%M-%S").sql

#echo "Clear mysql"
#cd $GOPATH/src/github.com/PPIO/go-ppio/test_scripts
#mysql -h 172.172.0.11 -uroot -p168168 < ./delete_mysql_data.sql

#echo "Clear user indexdata"
#cd $GOPATH/src/github.com/PPIO/go-ppio/
#rm -rf ./bin/user*/*.db
#rm -rf ./bin/user*/*.log
#rm -rf ./bin/user*/storage
#rm -rf ./bin/user*/wallet
#
#rm -rf ./bin/miner*/*.db
#rm -rf ./bin/miner*/*.log
#rm -rf ./bin/miner*/miner-*
#rm -rf ./bin/miner*/wallet
