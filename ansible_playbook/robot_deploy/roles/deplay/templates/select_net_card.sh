#!/usr/bin/env bash

robot_path=/root/.robot
start_script=${robot_path}/start.sh
flow_monitor_script=${robot_path}/robot_flow.sh
special_network=1

function check_net_card_speed(){
    name=${1}
    info=`ethtool ${name}`
    temp=${info#*'Speed: '}
    speed=${temp%%'Mb/s'*}

    if [ "${speed}"x = "10000"x ] || [ ${speed}x = "1000"x ]
    then
        echo "${name} speed ${speed} Mb/s"
        return 0
    else
        echo "${name} is not data line net card"
        return 1
    fi

}

content=`ip a|grep wan0@ |grep -v grep`
if [[ ${content} != "" ]]
then
    result=$(echo ${content} | grep "state DOWN")
    if [[ ${result} == "" ]]
    then
        temp=${content#*@}
        net_card=${temp%%': <'*}

        temp=$(echo ${net_card} | grep ".")
        if [ -n ${temp} ]
        then
            net_card=${net_card%%'.'*}
        fi

        special_network=0
    else
        echo "Can not find data line net card"
    fi
else
    card_name=`ip a |grep 'state UP' |grep -v grep`
    temp=${card_name#*' '}
    net_card=${temp%%': <'*}
fi

check_net_card_speed ${net_card}
if [ $? -eq 0 ]
then
    echo "Modify start robot script ${start_script}"
    if [ -e ${start_script} ]
    then
        command=`sed -n '/network_name=/p' ${start_script}`
        temp=${command#*'--network_name='}
        para=${temp%%' '*}
        sed -i "s/${para}/${net_card}/g" ${start_script}
        if [ ${special_network} -eq 0 ]
        then
            sed -i 's/--special_network//g' ${start_script}
        fi
    fi

    echo "Modify flow monitor robot script ${flow_monitor_script}"
    if [ -e ${flow_monitor_script} ]
    then
        sed -i "s/any/${net_card}/g" ${flow_monitor_script}
    fi
fi
