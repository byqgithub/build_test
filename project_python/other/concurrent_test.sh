#!/usr/bin/env bash

pcdn_dir="/home/workspace/go/src/github.com/PPIO/go-ppio/bin/"

download_list=("100M" "128K" "16M" "1G" "200M" "256M" "257K" "128K" "2M" "300M" "400M" "512M" "60M" "700M" "70M" "800M" "80M")

for i in ${download_list[@]}
do
    echo "download ${i}"
    ${pcdn_dir}/pcdn download add --url="http://192.168.50.207:8080/download/${i}" --file="/home/workspace/data/tmp/${i}" --backgroud --force
done

sleep 10

id_list=$(${pcdn_dir}/pcdn download list | grep -v "ID" | awk '{print $1}')
for id in ${id_list[@]}
do
    echo "delete task ${id}"
    ${pcdn_dir}/pcdn download delete ${id}
done
