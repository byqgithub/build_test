#!/usr/bin/env bash

declare -A cap_dict
cap_dict=([a20fb52264af4b99af3837a35f135cf1]=6.0
          [7ab1b1413e33407a833ba6b0dfc12cb7]=4.8
          [5014ab8654f74b9ca889b2609243c11c]=4.8
          [7d00bc7c84ae4c1ba49639000305933e]=10.0
          [d38b52517fcd4fc78a14afd9872b94a0]=6.0
          )

current_path=$(cd `dirname $0`; pwd)
for key in $(echo ${!cap_dict[*]})
do
    v=$(awk 'BEGIN{print "'${cap_dict[${key}]}'"*1000000000}')
    echo "machine id ${key}, replenish value: ${v}"
    ${current_path}/manager -d ${key} -c "/usr/bin/curl http://127.0.0.1:8888/percent/100000/percent_expire/5400/cap/${v}" -k ${current_path}/data/pi_backend/config/ecpri.pem
done

#          [9d8d20012eeb49b48782978126bf8fd6]=0.9
#          [832c188134fb448c839306303e2785e5]=6.0
#          [807ce34533e8483c8cd77932377a1649]=6.0
#          [139c9ba996fd42d88423b356605706c7]=0.8
#          [a20fb52264af4b99af3837a35f135cf1]=6.0
#          [7ab1b1413e33407a833ba6b0dfc12cb7]=4.8
#          [5014ab8654f74b9ca889b2609243c11c]=4.8
#          [7d00bc7c84ae4c1ba49639000305933e]=10.0
#          [d38b52517fcd4fc78a14afd9872b94a0]=6.0