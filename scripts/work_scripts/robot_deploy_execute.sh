#!/usr/bin/env bash

hosts=(33c56b5e57514a179e64ff5585cd3ed6
)

current_path=$(cd `dirname $0`; pwd)

for id in ${hosts[@]}
do
    echo "machine id:" ${id}
    ${current_path}/manager -d ${id} -c "nohup sh -c 'wget https://pi-miner.oss-cn-beijing.aliyuncs.com/tools/robot/robot_deploy.sh && /bin/bash /root/robot_deploy_back.sh' > robot_deploy.log 2>&1 &" -k ${current_path}/data/pi_backend/config/ecpri.pem
done


#current_path=$(cd `dirname $0`; pwd)
#machine_file=${current_path}/machine_id.txt
#touch ${machine_file}
#
#cat ${machine_file} | while read line
#do
#    echo "Machine id: ${line}"
#    ${current_path}/manager -d ${id} -c "nohup sh -c 'wget https://pi-miner.oss-cn-beijing.aliyuncs.com/tools/robot/robot_deploy.sh && /bin/bash /root/robot_deploy_back.sh' > robot_deploy.log 2>&1 &" -k ${current_path}/data/pi_backend/config/ecpri.pem
#done