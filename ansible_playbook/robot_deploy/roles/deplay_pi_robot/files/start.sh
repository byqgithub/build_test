#!/bin/bash

MY_PATH=$(dirname "$0")
cd ${MY_PATH}
MY_PATH="$(pwd)"

nohup $MY_PATH/pi-robot --http-addr=127.0.0.1:18889 --traffic-iface=test --log-level 3 > log.log 2>&1 &
