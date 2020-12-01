#!/bin/bash

MY_PATH=$(dirname "$0")
cd ${MY_PATH}
MY_PATH="$(pwd)"

nohup $MY_PATH/robot_flow.sh > flow_cap_log.log 2>&1 &
