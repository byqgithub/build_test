#!/usr/bin/env bash

hosts=(73e2be127b504ba190efede1aa078205
101c34b457274bc0afe877e104db70e6
993182d3cd544b7692d64930e69ec2bf
f678220777d6461b9875e08977e580e9
25866ca7db9641beac7bdda37039a188
7ab1b1413e33407a833ba6b0dfc12cb7
5014ab8654f74b9ca889b2609243c11c
0348bcca00ed493bad7a54632c270a2b
9086488090414d69bf57732ccb1e6bed
9e34b29f05bd4d40a231b3b5a1ba33c2
478fd690e87e4a74ad308ac7b717501c
426560bea5aa49f5bf7353d97268890d
3798e8fab3cb43e49152b90dfe08c229
a1f28bb2339b4a6097ea5e837026168b
65baad06e563445b9077c6449c17fddd
)

current_path=$(cd `dirname $0`; pwd)

for id in ${hosts[@]}
do
    echo "machine id:" ${id}
#    ${current_path}/manager -d ${id} -c "systemctl stop pi-robot" -k ${current_path}/data/pi_backend/config/ecpri.pem
#    ${current_path}/manager -d ${id} -c "cd /root/.robot && rm -rf pi-robot && wget https://pi-miner.oss-cn-beijing.aliyuncs.com/tools/robot/pi-robot && chmod 777 pi-robot" -k ${current_path}/data/pi_backend/config/ecpri.pem
#    ${current_path}/manager -d ${id} -c "systemctl start pi-robot" -k ${current_path}/data/pi_backend/config/ecpri.pem
    ${current_path}/manager -d ${id} -c "ps -ef|grep robot |grep -v grep" -k ${current_path}/data/pi_backend/config/ecpri.pem
    ${current_path}/manager -d ${id} -c "/root/.robot/pi-robot version" -k ${current_path}/data/pi_backend/config/ecpri.pem
    ${current_path}/manager -d ${id} -c "md5sum /root/.robot/pi-robot" -k ${current_path}/data/pi_backend/config/ecpri.pem
done