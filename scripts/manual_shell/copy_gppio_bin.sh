#!/usr/bin/env bash

bin_dir=/home/ppio_chain_bin/
mkdir -p ${bin_dir}
cd ${GOPATH}/src/github.com/PPIO/ppio-chain/

echo "Copy ppio-chain executable env"
cp -rP  gppio* ${bin_dir}
cp -rP  keydir ${bin_dir}
cp -rP  lib ${bin_dir}
cp -rP  nf ${bin_dir}
cp -rP  conf ${bin_dir}
echo "Copy done"