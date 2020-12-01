#!/usr/bin/env bash

echo $(cat /etc/machine-id)

process_name=("pi-robot-client" "flow_cap" "robot_flow.sh" "pi-robot")
for name in ${process_name[@]}
do
   echo "process name:" ${name}
   for pid in `ps -ef | grep ${name} | grep -v grep | awk '{print $2}'`
   do
      kill -9 ${pid}
   done
done

systemctl stop pi-robot

mkdir -p /root/.robot/
wget https://pi-miner.oss-cn-beijing.aliyuncs.com/tools/robot/pi-robot -O /root/.robot/pi-robot
chmod 777 /root/.robot/pi-robot

cat << EOF > /etc/systemd/system/pi-robot.service
[Unit]
Description= robot for pi yun
After=network-online.target firewalld.service
StartLimitIntervalSec = 60
Starteimitnurst = 1

[Service]
Type = simple
#替换-config的参数为真实路径，测试时可以指定--log-level 5，否则不用指定
ExecStart = /root/.robot/pi-robot --config https://pi-miner.oss-cn-beijing.aliyuncs.com/tools/robot/config.toml
ExecStop = /usr/bin/pkill pi-robot
RestartSec = 10
TimeoutStopSec = 5
Restart = on-failure

EOF

systemctl enable pi-robot
systemctl start pi-robot
