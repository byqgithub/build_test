#!/bin/bash

source /etc/profile

cd $GOPATH/src/github.com/PPIO/go-ppio/

file_time=poss_$(date "+%Y-%m-%d_%H_%M-%S")
echo $file_time
mkdir -p /tmp/test_log/log_${file_time}

screen -dmS "ppiox.miner0"  -L -Logfile /tmp/test_log/log_${file_time}/miner0.log      ./bin/miner daemon start --datadir=/tmp/miner0 --verbose
sleep 5
screen -dmS "ppiox.miner1"  -L -Logfile /tmp/test_log/log_${file_time}/miner1.log      ./bin/miner daemon start --datadir=/tmp/miner1 --verbose
sleep 5
screen -dmS "ppiox.miner2"  -L -Logfile /tmp/test_log/log_${file_time}/miner2.log      ./bin/miner daemon start --datadir=/tmp/miner2 --verbose
sleep 5
screen -dmS "ppiox.miner3"  -L -Logfile /tmp/test_log/log_${file_time}/miner3.log      ./bin/miner daemon start --datadir=/tmp/miner3 --verbose
sleep 5
screen -dmS "ppiox.miner4"  -L -Logfile /tmp/test_log/log_${file_time}/miner4.log      ./bin/miner daemon start --datadir=/tmp/miner4 --verbose
sleep 5
screen -dmS "ppiox.miner5"  -L -Logfile /tmp/test_log/log_${file_time}/miner5.log      ./bin/miner daemon start --datadir=/tmp/miner5 --verbose
sleep 5
screen -dmS "ppiox.miner6"  -L -Logfile /tmp/test_log/log_${file_time}/miner6.log      ./bin/miner daemon start --datadir=/tmp/miner6 --verbose
sleep 5
screen -dmS "ppiox.miner7"  -L -Logfile /tmp/test_log/log_${file_time}/miner7.log      ./bin/miner daemon start --datadir=/tmp/miner7 --verbose
sleep 5

screen -dmS "ppiox.user0"   -L -Logfile /tmp/test_log/log_${file_time}/user0.log       ./bin/poss start-daemon --datadir=/tmp/user0 --verbose
screen -dmS "ppiox.user1"   -L -Logfile /tmp/test_log/log_${file_time}/user1.log       ./bin/poss start-daemon --datadir=/tmp/user1 --verbose

screen -ls

