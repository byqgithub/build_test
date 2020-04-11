#!/bin/bash

echo "Import Object"
cd $GOPATH/src/github.com/PPIO/go-ppio/
./bin/ppio object import --rpcport=18060 /home/tmp/ppio.txt
screen -ls
read -n 1 -p "Press enter to continue..."


echo "Put Object"
./bin/ppio object put --rpcport=18060 --copies=1 --duration=86400 --gasprice=100 --acl=public 8aecec0f60c6b737bdc89686c189cb2073e8f16689933142b3c85246789f4805
screen -ls
read -n 1 -p "Press enter to continue..."

echo "Object status"
./bin/ppio object status --rpcport=18060 8aecec0f60c6b737bdc89686c189cb2073e8f16689933142b3c85246789f4805
screen -ls
read -n 1 -p "Press enter to continue..."

echo "Get Object"
./bin/ppio object get --rpcport=18060 --gasprice=100 --owner=002508021221033fb36e1471d2153d0759e14386c6c294b1ad09244841ee8d043eadd1bfe7baaa  8aecec0f60c6b737bdc89686c189cb2073e8f16689933142b3c85246789f4805
screen -ls
read -n 1 -p "Press enter to continue..."

echo "Storage Object"
./bin/ppio storage object --rpcport=18060 8aecec0f60c6b737bdc89686c189cb2073e8f16689933142b3c85246789f4805
screen -ls
read -n 1 -p "Press enter to continue..."

echo "Copy Object"
./bin/ppio object auth --rpcport=18060 --duration=86400 --accessor=002508021221024d8a69222ab1b305aa6abd5615058ed0e7e9f4da04e190284bbfb5fae968b348  8aecec0f60c6b737bdc89686c189cb2073e8f16689933142b3c85246789f4805
./bin/ppio object copy --rpcport=18061 --copies=1 --duration=86400 --gasprice=100 --acl=public --auth=9570f05335108a86a06401d23f1ab4f91bd2950e5e5c3698711414970c3cbfc807a5d3d1f690955003e37e2f83655105c972697997213b782f3cc138485a9095008aecec0f60c6b737bdc89686c189cb2073e8f16689933142b3c85246789f480527000000002508021221033fb36e1471d2153d0759e14386c6c294b1ad09244841ee8d043eadd1bfe7baaa27000000002508021221024d8a69222ab1b305aa6abd5615058ed0e7e9f4da04e190284bbfb5fae968b348b73d665c00000000 --owner=002508021221033fb36e1471d2153d0759e14386c6c294b1ad09244841ee8d043eadd1bfe7baaa   8aecec0f60c6b737bdc89686c189cb2073e8f16689933142b3c85246789f4805
screen -ls
read -n 1 -p "Press enter to continue..."

echo "Renew Object"
./bin/ppio object renew --rpcport=18060 --copies=1 --duration=86400 --gasprice=100 --acl=public 8aecec0f60c6b737bdc89686c189cb2073e8f16689933142b3c85246789f4805
screen -ls
read -n 1 -p "Press enter to continue..."

