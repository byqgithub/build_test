#!/usr/bin/env bash

miner_num=$(($1))
miner_type=$2
echo "miner number:" $1

if [ "256G" = $2 ]
then
    plot_limit="128"
    plot_count="256"
    plot_size="1G"
elif [ "1T" = $2 ]
then
    plot_limit="128"
    plot_count="256"
    plot_size="4G"
elif [ "8T" = $2 ]
then
    plot_limit="1024"
    plot_count="2048"
    plot_size="4G"
else
    plot_limit="2"
    plot_count="4"
    plot_size="128M"
fi

echo "plot_limit: ${plot_limit}"
echo "plot_count: ${plot_count}"
echo "plot_size: ${plot_size}"

cd $GOPATH/src/github.com/PPIO/go-ppio/bin
num=0
while(( ${num}<${miner_num} ))
do
    rpcport=`expr 18050 + ${num}`
    echo "miner rpc: ${rpcport}"
#    ./miner storage addplotdir miner-plot-1 ${plot_limit} --rpcport=${rpcport}
#    ./miner storage addplotdir miner-plot-2 ${plot_limit} --rpcport=${rpcport}
#
#    ./miner storage plotsize ${plot_size} --rpcport=${rpcport}
#
#    ./miner storage adjustplotcount ${plot_count} false --rpcport=${rpcport}
    let "num++"
done