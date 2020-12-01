#!/bin/bash

cat << EOF > /var/pedge.sh
#!/bin/bash
echo 'pi_flow_robot up_bandwidth='
EOF

chmod u+x /var/pedge.sh

TIME=6

while [ 0 -lt 1 ]
do
  tcpdump -i any -nn dst port 9960 2>/dev/null | awk {'print $NF'} > /tmp/tcp &
  sleep $TIME
  kill -9 $(pidof tcpdump)
  b_count=$(cat /tmp/tcp | wc -l)
  m=$(( $b_count * 1400 / $TIME ))
  sed -i "s/=.*'/=$m'/g" /var/pedge.sh
done