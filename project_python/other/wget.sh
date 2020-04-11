#!/usr/bin/env bash

function finish() {
     expressvpn disconnect
     echo "process exit" >> /home/test/log/wget.log
     echo " " >> /home/test/log/wget.log
     echo " " >> /home/test/log/wget.log
     echo " " >> /home/test/log/wget.log
     echo " " >> /home/test/log/wget.log

}

trap finish EXIT

location=${1}

mkdir -p /home/test/log/
echo "START" >> /home/test/log/wget.log
python /home/test/wget.py ${location} >> /home/test/log/wget.log
echo "END" >> /home/test/log/wget.log
echo " " >> /home/test/log/wget.log
echo " " >> /home/test/log/wget.log
