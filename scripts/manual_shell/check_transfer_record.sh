#!/usr/bin/env bash

echo "Check user0 transfer record"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"TransferRecord","params":[{"accountID":"ppio1RE2Ci5NkWeB8RCtktVvQfWjnbRymYTGLp","start":0,"limit":50}]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check user1 transfer record"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"TransferRecord","params":[{"accountID":"ppio1HSzb3VupRUsc78jqffo3FT2nq2MFbHvqr","start":0,"limit":50}]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check user2 transfer record"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"TransferRecord","params":[{"accountID":"ppio1T2gap1w1FZWK6dv63ef32KsCN9t4Cpt41","start":0,"limit":50}]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check miner0 transfer record"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"TransferRecord","params":[{"accountID":"ppio1KgqNbxTiNqKyaahLFjSGGfK2WuJNR4HFb","start":0,"limit":50}]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check miner1 transfer record"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"TransferRecord","params":[{"accountID":"ppio1QcM4YmKQ55q6NKFT7XR1ek21H3eYWE9zP","start":0,"limit":50}]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check miner2 transfer record"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"TransferRecord","params":[{"accountID":"ppio1QkS9abTtBsSCFtMdBqqBFsJsBpcZuyc7q","start":0,"limit":50}]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check miner3 transfer record"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"TransferRecord","params":[{"accountID":"ppio1awPPtYeyV1KsDLUuEHKHV9StKGycsg8f9","start":0,"limit":50}]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check miner4 transfer record"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"TransferRecord","params":[{"accountID":"ppio1XHf9Pain1hoH11jfDc94K5Z1u4NeEpVdW","start":0,"limit":50}]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check indexer0 transfer record"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"TransferRecord","params":[{"accountID":"ppio1LY41TGNpbXKHaHMjSJXrry8st4ychWpHf","start":0,"limit":50}]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check indexer1 transfer record"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"TransferRecord","params":[{"accountID":"ppio1D2X5chm5czMMxpibPrinkqgSAvQGCpdWE","start":0,"limit":50}]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check verifier0 transfer record"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"TransferRecord","params":[{"accountID":"ppio1QJND7L5GePzuDLTm7g4ci9rJLyAtBKXRY","start":0,"limit":50}]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check verifier1 transfer record"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"TransferRecord","params":[{"accountID":"ppio1GoscFNMQfawQB7vDTWtvrhM2uz5pDuajj","start":0,"limit":50}]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check issuance transfer record"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"TransferRecord","params":[{"accountID":"ppio1TNPH5mnm7EVQTVCXnPXaHdsoUmXxNx781","start":0,"limit":50}]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check provident transfer record"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"TransferRecord","params":[{"accountID":"ppio1WvBd3SRwrnUQRMtPZGgUMteViRW3a5EdF","start":0,"limit":50}]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo "Check cpool transfer record"
curl -X POST -H 'content-type:text/json;' --data '{"id":1,"jsonrpc":"2.0","method":"TransferRecord","params":[{"accountID":"ppio1NkZvLjCvJkN5789MFzsn4cNSQkc3JWd2J","start":0,"limit":50}]}' http://127.0.0.1:18030/rpc
echo ""
echo "------------------------------------"

echo ""
echo ""
echo ""
echo ""