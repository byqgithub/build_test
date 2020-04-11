#!/bin/bash

source /etc/profile
#echo "restart redis-sever"
#service redis-server restart

#echo "Update mysql"
#cd $GOPATH/src/github.com/PPIO/go-ppio/
#mysql -h 172.172.0.11 -uroot -p168168 -e "CREATE DATABASE IF NOT EXISTS ppio;"
#mysql -h 172.172.0.11 -uroot -p168168 -D ppio < ./service/indexer/assets/ppio.sql

#echo "Start gppio"
#cd $GOPATH/src/github.com/PPIO/ppio-chain/
#./launch.sh


echo "Start ppio server"
cd $GOPATH/src/github.com/PPIO/go-ppio/

file_time=ppio_$(date "+%Y-%m-%d_%H-%M-%S")
echo $file_time
mkdir -p /tmp/test_log/log_${file_time}

#start ppio servers on a node
#screen -dmS "ppiox.redis-server" redis-server
screen -dmS "ppiox.center"       -L -Logfile /tmp/test_log/log_${file_time}/center.log        ./bin/center --datadir=/tmp/center --verbose
screen -dmS "ppiox.bootstrap"    -L -Logfile /tmp/test_log/log_${file_time}/bootstrap.log     ./bin/bootstrap --datadir=/tmp/bootstrap --verbose
screen -dmS "ppiox.indexer"      -L -Logfile /tmp/test_log/log_${file_time}/indexer.log       ./bin/indexer --datadir=/tmp/indexer --verbose #--config=./cmd/indexer/indexer.json
#./cmd/scripts/indexer/load_ppio_miners.sh
screen -dmS "ppiox.verifier"     -L -Logfile /tmp/test_log/log_${file_time}/verifier.log      ./bin/verifier --datadir=/tmp/verifier --verbose
#screen -dmS "ppiox.gateway"      -L -Logfile /tmp/test_log/log_${file_time}/gateway.log       ./bin/gateway  --datadir=/tmp/gateway --verbose
screen -ls


#echo "Deposit"
#cd $GOPATH/src/github.com/PPIO/ppio-chain/
#./transfer_center2provident.sh
#sleep 5
#./transfer_center2accounts.sh
#sleep 60
#./transfer_accounts2holder.sh
#sleep 30


#echo "Check balance"
#cd $GOPATH/src/github.com/PPIO/go-ppio/
#./build/scripts/demo/checkBalance.sh

