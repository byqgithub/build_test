#!/usr/bin/env bash

contractId=$1
echo ${contractId}

echo "Check user0 storage detail"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"StorageDetail","params":[{"accountID":"ppio1RE2Ci5NkWeB8RCtktVvQfWjnbRymYTGLp", "contractIDs": ["'${contractId}'"]}]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check user1 storage detail"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"StorageDetail","params":[{"accountID":"ppio1HSzb3VupRUsc78jqffo3FT2nq2MFbHvqr", "contractIDs": ["'${contractId}'"]}]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check user2 storage detail"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"StorageDetail","params":[{"accountID":"ppio1T2gap1w1FZWK6dv63ef32KsCN9t4Cpt41", "contractIDs": ["'${contractId}'"]}]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check miner0 storage detail"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"StorageDetail","params":[{"accountID":"ppio1KgqNbxTiNqKyaahLFjSGGfK2WuJNR4HFb", "contractIDs": ["'${contractId}'"]}]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check miner1 storage detail"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"StorageDetail","params":[{"accountID":"ppio1QcM4YmKQ55q6NKFT7XR1ek21H3eYWE9zP", "contractIDs": ["'${contractId}'"]}]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check miner2 storage detail"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"StorageDetail","params":[{"accountID":"ppio1QkS9abTtBsSCFtMdBqqBFsJsBpcZuyc7q", "contractIDs": ["'${contractId}'"]}]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check miner3 storage detail"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"StorageDetail","params":[{"accountID":"ppio1awPPtYeyV1KsDLUuEHKHV9StKGycsg8f9", "contractIDs": ["'${contractId}'"]}]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check indexer storage detail"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"StorageDetail","params":[{"accountID":"ppio1LY41TGNpbXKHaHMjSJXrry8st4ychWpHf", "contractIDs": ["'${contractId}'"]}]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check verifier storage detail"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"StorageDetail","params":[{"accountID":"ppio1QJND7L5GePzuDLTm7g4ci9rJLyAtBKXRY", "contractIDs": ["'${contractId}'"]}]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

#echo "Check cpool storage detail"
#curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"StorageDetail","params":[{"accountID":"ppio1GoscFNMQfawQB7vDTWtvrhM2uz5pDuajj", "contractIDs": ["'${contractId}'"]}]}' http://127.0.0.1:18030/rpc
#echo "------------------------------------"
echo ""
echo ""
echo ""
echo ""