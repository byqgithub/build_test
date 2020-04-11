#!/usr/bin/env bash

source /etc/profile
script_path=$(cd `dirname $0`; pwd)
echo "current path: " ${script_path}

if [ $# -ne 2 ]
then
    bucket="user0bucket"
    key="/test/test.txt_0"
    body="${script_path}/1G"
else
    bucket=${1}
    key=${2}
    body=${3}
fi

echo "key: ${key}"
echo "body: ${body}"

cd ${script_path}

#num=0
#miner_num=10
#while(( ${num}<${miner_num} ))
#do
#    start_time=$(date "+%Y-%m-%d_%H-%M-%S")
#    ./poss put-object --bucket=${bucket} --key=${key}_${num} --body=${body} --chiprice=200 --copies=5 --expires=2019-12-12 --rpcport=18060
#    end_time=$(date "+%Y-%m-%d_%H-%M-%S")
#    echo "start time: ${start_time}"
#    echo "end time: ${end_time}"
#    echo "execute times: ${num}"    "start time: ${start_time}"    "end time: ${end_time}" >> ./record.txt
#    let "num++"
#done

num=0
miner_num=12
while(( ${num}<${miner_num} ))
do
    start_time=$(date "+%Y-%m-%d_%H-%M-%S")
    ./poss get-object --bucket=${bucket} --key=${key} --outfile=${script_path}/outfile_${num} --chiprice=200 --rpcport=18060
    end_time=$(date "+%Y-%m-%d_%H-%M-%S")
    echo "start time: ${start_time}"
    echo "end time: ${end_time}"
    echo "execute times: ${num}"    "start time: \"${start_time}\","    "end time: \"${end_time}\"," >> ./record.txt
    let "num++"
done

./poss sync-objects --rpcport=18060
./poss list-objects --bucket=${bucket} --rpcport=18060 > ./list_objects.txt
./poss list-tasks --rpcport=18060 > ./list_tasks.txt

cd -