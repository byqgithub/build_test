#!/bin/bash

cd $GOPATH/src/github.com/PPIO/go-ppio/

file_time=poss_$(date "+%Y-%m-%d_%H_%M-%S")
echo $file_time
mkdir -p $(pwd)/test_log/log_${file_time}

screen -dmS "ppiox.miner0"  -L -Logfile $(pwd)/test_log/log_${file_time}/miner0.log      ./bin/miner daemon start --datadir=./bin/miner0 --verbose
#sleep 5
screen -dmS "ppiox.miner1"  -L -Logfile $(pwd)/test_log/log_${file_time}/miner1.log      ./bin/miner daemon start --datadir=./bin/miner1 --verbose # --storage-chiprice=80 --download-chiprice=80
#sleep 5
screen -dmS "ppiox.miner2"  -L -Logfile $(pwd)/test_log/log_${file_time}/miner2.log      ./bin/miner daemon start --datadir=./bin/miner2 --verbose
#sleep 5
# screen -dmS "ppiox.miner3"  -L -Logfile $(pwd)/test_log/log_${file_time}/miner3.log      ./bin/miner daemon start --datadir=./bin/miner3 --verbose
#sleep 5
# screen -dmS "ppiox.miner4"  -L -Logfile $(pwd)/test_log/log_${file_time}/miner4.log      ./bin/miner daemon start --datadir=./bin/miner4 --verbose
#sleep 5
#screen -dmS "ppiox.miner5"  -L -Logfile $(pwd)/test_log/log_${file_time}/miner5.log      ./bin/miner daemon start --datadir=./bin/miner5 --verbose
#sleep 5
#screen -dmS "ppiox.miner6"  -L -Logfile $(pwd)/test_log/log_${file_time}/miner6.log      ./bin/miner daemon start --datadir=./bin/miner6 --verbose
#sleep 5
#screen -dmS "ppiox.miner7"  -L -Logfile $(pwd)/test_log/log_${file_time}/miner7.log      ./bin/miner daemon start --datadir=./bin/miner7 --verbose
sleep 5


screen -dmS "ppiox.user0"   -L -Logfile $(pwd)/test_log/log_${file_time}/user0.log       ./bin/poss start-daemon --datadir=./bin/user0 --verbose
screen -dmS "ppiox.user1"   -L -Logfile $(pwd)/test_log/log_${file_time}/user1.log       ./bin/poss start-daemon --datadir=./bin/user1 --verbose
#screen -dmS "ppiox.user2"   -L -Logfile $(pwd)/test_log/log_${file_time}/user2.log       ./bin/poss start-daemon --datadir=./bin/user2 --verbose
#screen -dmS "ppiox.user3"   -L -Logfile $(pwd)/test_log/log_${file_time}/user3.log       ./bin/poss start-daemon --datadir=./bin/user3 --verbose

screen -ls

