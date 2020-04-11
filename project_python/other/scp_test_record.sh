#!/usr/bin/env bash

declare -A ip_dict
ip_dict=([American]="45.77.146.85"
         [British]="217.163.11.33"
         [Germany]="136.244.85.203"
         [HongKong]="47.90.73.58"
         [Canada]="155.138.144.6"
         [Netherlands]="95.179.128.178")

current_dir=$(cd `dirname $0`; pwd)

for location in $(echo ${!ip_dict[*]})
do
    folder=${current_dir}/${location}/record_$(date "+%Y-%m-%d_%H-%M-%S")
    mkdir -p ${folder}
    sshpass -p testvpn1 scp root@${ip_dict[${location}]}:/home/test/*_record.log ${folder}
    sshpass -p testvpn1 scp root@${ip_dict[${location}]}:/home/test/log/wget.log ${folder}
done