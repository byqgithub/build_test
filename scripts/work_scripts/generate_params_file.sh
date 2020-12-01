#!/usr/bin/env bash

current_path=$(cd `dirname $0`; pwd)
params_file=${current_path}/test.txt

function rand(){
    min=$1
    max=$(($2-$min+1))
    num=$(($RANDOM+1000000000))
    echo $(($num%$max+$min))
}

cat ${params_file} | while read line
do
    # echo ${line}
    machine_id=$(echo ${line} | awk '{print $1}')
    work_interface=$(echo ${line} | awk '{print $2}')
    detect_interface=$(echo ${line} | awk '{print $3}')
    bandwidth=$(echo ${line} | awk '{print $4}')
    hour=$(rand 6 12)
    minute=$(rand 0 59)
    # echo "${hour}:${minute}"
    echo "machine_id ${machine_id}  work_interface ${work_interface} detect_interface ${detect_interface} time:${hour}:${minute}"

    cat << EOF >> all_robot_params_conf_1.txt
[${machine_id}]
 machines = [
 "d2f09d14cb6240b7bfb0d59f322090df",
 "ee616ffc38e84c65b584719b13af0bc5",
 "9f50025d04054c53abf859a7dccfb177",
 "e4d57d0b5ad54d85abe5e9adc78a5fe7"
 ]
 daily_begin = "${hour}:${minute}"
 expect_bandwidth = ${bandwidth}
 duration = 5400
 work_interface = "${work_interface}"
 detect_interface = ["${detect_interface}"]

EOF
done
