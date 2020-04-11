#!/bin/bash

cd $GOPATH/src/github.com/PPIO/go-ppio/

file_time=user_miner_$(date "+%Y-%m-%d_%H_%M-%S")
echo $file_time
mkdir -p $(pwd)/test_log/log_${file_time}

screen -dmS "ppiox.miner0"  -L -Logfile $(pwd)/test_log/log_${file_time}/miner0.log      ./bin/miner daemon start --datadir=./miner0
sleep 5
screen -dmS "ppiox.miner1"  -L -Logfile $(pwd)/test_log/log_${file_time}/miner1.log      ./bin/miner daemon start --datadir=./miner1
#sleep 5
#screen -dmS "ppiox.miner2"  -L -Logfile $(pwd)/test_log/log_${file_time}/miner2.log      ./bin/miner daemon start --datadir=./miner2
#sleep 5
#screen -dmS "ppiox.miner3"  -L -Logfile $(pwd)/test_log/log_${file_time}/miner3.log      ./bin/miner daemon start --datadir=./miner3
#sleep 5
#screen -dmS "ppiox.miner4"  -L -Logfile $(pwd)/test_log/log_${file_time}/miner4.log      ./bin/miner daemon start --datadir=./miner4
#sleep 5
#screen -dmS "ppiox.miner5"  -L -Logfile $(pwd)/test_log/log_${file_time}/miner5.log      ./bin/miner daemon start --datadir=./miner5
#sleep 5

screen -dmS "ppiox.user0"   -L -Logfile $(pwd)/test_log/log_${file_time}/user0.log       ./bin/ppio --datadir=./user0
screen -dmS "ppiox.user1"   -L -Logfile $(pwd)/test_log/log_${file_time}/user1.log       ./bin/ppio --datadir=./user1

screen -ls

