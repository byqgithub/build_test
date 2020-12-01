#!/usr/bin/env bash

declare -A cap_dict
cap_dict=([4a8eaf0d9dd242ecb3778140d27084b5]=1.3
          )

current_path=$(cd `dirname $0`; pwd)
for key in $(echo ${!cap_dict[*]})
do
    v=$(awk 'BEGIN{print "'${cap_dict[${key}]}'"*1000000000}')
    echo "machine id ${key}, cap value: ${v}"
    ${current_path}/manager -d ${key} -c "sed -i 's/cap\/.*/cap\/${v}/g' /usr/local/scripts/curl.sh" -k ${current_path}/data/pi_backend/config/ecpri.pem

    tmp=$(${current_path}/manager -d ${key} -c "cat /usr/local/scripts/curl.sh | grep -P '.*flow/([0-9]+)/.*'| cut -d '/' -f 8" -k ${current_path}/data/pi_backend/config/ecpri.pem)
    ${current_path}/manager -d ${key} -c "sed -i 's/${tmp}/${v}/g' /usr/local/scripts/curl.sh" -k ${current_path}/data/pi_backend/config/ecpri.pem
done
