#!/bin/bash

cd $GOPATH/src/github.com/PPIO/go-ppio/

echo "Check user0 account"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"QueryAccount","params":["ppio1RE2Ci5NkWeB8RCtktVvQfWjnbRymYTGLp"]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check user1 account"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"QueryAccount","params":["ppio1HSzb3VupRUsc78jqffo3FT2nq2MFbHvqr"]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check user2 account"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"QueryAccount","params":["ppio1T2gap1w1FZWK6dv63ef32KsCN9t4Cpt41"]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check miner0 account"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"QueryAccount","params":["ppio1KgqNbxTiNqKyaahLFjSGGfK2WuJNR4HFb"]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check miner1 account"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"QueryAccount","params":["ppio1QcM4YmKQ55q6NKFT7XR1ek21H3eYWE9zP"]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check miner2 account"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"QueryAccount","params":["ppio1QkS9abTtBsSCFtMdBqqBFsJsBpcZuyc7q"]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check miner3 account"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"QueryAccount","params":["ppio1awPPtYeyV1KsDLUuEHKHV9StKGycsg8f9"]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check miner4 account"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"QueryAccount","params":["ppio1XHf9Pain1hoH11jfDc94K5Z1u4NeEpVdW"]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check indexer0 account"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"QueryAccount","params":["ppio1LY41TGNpbXKHaHMjSJXrry8st4ychWpHf"]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check indexer1 account"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"QueryAccount","params":["ppio1J8frj1RMxBVR51mJu7tBeCWbp1rfSkxca"]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check verifier0 account"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"QueryAccount","params":["ppio1QJND7L5GePzuDLTm7g4ci9rJLyAtBKXRY"]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check verifier1 account"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"QueryAccount","params":["ppio1GoscFNMQfawQB7vDTWtvrhM2uz5pDuajj"]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check issuance account"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"QueryAccount","params":["ppio1TNPH5mnm7EVQTVCXnPXaHdsoUmXxNx781"]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check provident account"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"QueryAccount","params":["ppio1WvBd3SRwrnUQRMtPZGgUMteViRW3a5EdF"]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check holder account"
curl -X POST -H 'content-type:application/json;' --data '{"address":"ppio1QkQ8MRDnX8ynbmniUopSkbhzpqXZ3XKjF"}' http://127.0.0.1:8685/v1/user/accountstate
echo ""
echo "------------------------------------"

echo "Check cpool account"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"QueryAccount","params":["ppio1NkZvLjCvJkN5789MFzsn4cNSQkc3JWd2J"]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo ""
echo ""
echo ""
echo ""

#curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"Withdraw","params":[{"accountID": "ppio1RE2Ci5NkWeB8RCtktVvQfWjnbRymYTGLp", "amount": "300000000000"}]}' http://127.0.0.1:18030/rpc

#curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"WithdrawRecord","params":[{"accountID": "ppio1RE2Ci5NkWeB8RCtktVvQfWjnbRymYTGLp", "start": "0", "limit": "50"}]}' http://127.0.0.1:18030/rpc

#curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"AllValidMiner"}'  http://ad04b30b910c311e9b71c02d26ce9aff-567092461.us-west-2.elb.amazonaws.com:18030/rpc

#curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"AllValidMiner"}'  http://127.0.0.1:18030/rpc