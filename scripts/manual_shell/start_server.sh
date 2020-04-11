#!/bin/bash

#echo "restart redis-sever"
#service redis-server restart

#echo "Update mysql"
#cd $GOPATH/src/github.com/PPIO/go-ppio/
#mysql -h 172.172.0.11 -uroot -p168168 -e "CREATE DATABASE IF NOT EXISTS ppio;"
#mysql -h 172.172.0.11 -uroot -p168168 -D ppio < ./service/indexer/assets/ppio.sql

echo "Start gppio"
cd $GOPATH/src/github.com/PPIO/ppio-chain/
./launch.sh
sleep 10


echo "Start ppio server"
cd $GOPATH/src/github.com/PPIO/go-ppio/

file_time=ppio_$(date "+%Y-%m-%d_%H-%M-%S")
echo $file_time
mkdir -p $(pwd)/test_log/log_${file_time}

screen -dmS "ppiox.center"       -L -Logfile $(pwd)/test_log/log_${file_time}/center.log      ./bin/center --datadir=$(pwd)/bin/center_datadir --verbose
sleep 5
screen -dmS "ppiox.bootstrap0"    -L -Logfile $(pwd)/test_log/log_${file_time}/bootstrap0.log   ./bin/bootstrap --datadir=$(pwd)/bin/bootstrap0_datadir --verbose
#screen -dmS "ppiox.bootstrap1"    -L -Logfile $(pwd)/test_log/log_${file_time}/bootstrap1.log   ./bin/bootstrap --datadir=$(pwd)/bin/bootstrap1_datadir --verbose
sleep 5
screen -dmS "ppiox.indexer0"      -L -Logfile $(pwd)/test_log/log_${file_time}/indexer0.log     ./bin/indexer --datadir=$(pwd)/bin/indexer0_datadir --verbose --holder-passphrase=passphrase # --config=$(pwd)/bin/indexer0_datadir/indexer.conf
#screen -dmS "ppiox.indexer1"      -L -Logfile $(pwd)/test_log/log_${file_time}/indexer1.log     ./bin/indexer --datadir=$(pwd)/bin/indexer1_datadir --config=$(pwd)/bin/indexer1_datadir/indexer.conf --verbose
sleep 5
screen -dmS "ppiox.verifier0"     -L -Logfile $(pwd)/test_log/log_${file_time}/verifier0.log    ./bin/verifier --datadir=$(pwd)/bin/verifier0_datadir --verbose
#screen -dmS "ppiox.verifier1"     -L -Logfile $(pwd)/test_log/log_${file_time}/verifier1.log    ./bin/verifier --datadir=$(pwd)/bin/verifier1_datadir --verbose

screen -ls


#echo "Deposit"
#cd $GOPATH/src/github.com/PPIO/ppio-chain/
#./transfer_center2accounts.sh
#sleep 60
#./transfer_accounts2holder.sh


#echo "Check balance"
#cd $GOPATH/src/github.com/PPIO/go-ppio/
#./build/scripts/demo/checkBalance.sh

