#!/bin/bash
source /etc/profile
go_path=$1
script_path=$2
timestamp=$3

echo "Update mysql"
cd ${go_path}/src/github.com/PPIO/go-ppio/service/indexer/assets/
mysql -h 172.172.0.11 -uroot -p168168 -D ppio < ./ppio.sql

echo "Start gppio"
cd ${go_path}/src/github.com/PPIO/gppio/
./launch.sh


echo "Start ppio server"
cd ${go_path}/src/github.com/PPIO/go-ppio/

file_time=${timestamp}
echo $file_time
mkdir -p ${script_path}/test_log/${file_time}

# start ppio servers on a node
# screen -dmS "ppiox.redis-server" redis-server
service redis-server restart
screen -dmS "ppiox.center"       -L -Logfile ${script_path}/test_log/${file_time}/center.log        ./bin/center
screen -dmS "ppiox.bootstrap"    -L -Logfile ${script_path}/test_log/${file_time}/bootstrap.log     ./bin/bootstrap
screen -dmS "ppiox.indexer"      -L -Logfile ${script_path}/test_log/${file_time}/indexer.log       ./bin/indexer --config=${script_path}/config/indexer/indexer.json
# ./cmd/scripts/indexer/load_ppio_miners.sh
screen -dmS "ppiox.verifier"     -L -Logfile ${script_path}/test_log/${file_time}/verifier.log      ./bin/verifier
screen -dmS "ppiox.paymentproxy" -L -Logfile ${script_path}/test_log/${file_time}/paymentproxy.log  ./bin/paymentproxy
screen -dmS "ppiox.gateway"      -L -Logfile ${script_path}/test_log/${file_time}/gateway.log       ./bin/gateway
screen -ls


echo "Deposit"
cd ${go_path}/src/github.com/PPIO/gppio/
./transfer_center2accounts.sh
sleep 60
./transfer_accounts2holder.sh
sleep 30s


# echo "Check balance"
# cd ${go_path}/src/github.com/PPIO/go-ppio/
# ./build/scripts/demo/checkBalance.sh

