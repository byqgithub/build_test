#!/usr/bin/env bash

process_name=("pi-robot-client" "flow_cap" "robot_flow.sh")
for name in ${process_name[@]}
do
   echo "process name:" ${name}
   for pid in `ps -ef | grep ${name} | grep -v grep | awk '{print $2}'`
   do
      kill -9 ${pid}
   done
done
