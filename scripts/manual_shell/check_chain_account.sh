#!/usr/bin/env bash

echo "Check user0 account"
curl -X POST -H 'content-type:application/json;' --data '{"address":"ppio1RE2Ci5NkWeB8RCtktVvQfWjnbRymYTGLp"}' http://127.0.0.1:8685/v1/user/accountstate
echo ""
echo "------------------------------------"

echo "Check user1 account"
curl -X POST -H 'content-type:application/json;' --data '{"address":"ppio1HSzb3VupRUsc78jqffo3FT2nq2MFbHvqr"}' http://127.0.0.1:8685/v1/user/accountstate
echo ""
echo "------------------------------------"

echo "Check user2 account"
curl -X POST -H 'content-type:application/json;' --data '{"address":"ppio1T2gap1w1FZWK6dv63ef32KsCN9t4Cpt41"}' http://127.0.0.1:8685/v1/user/accountstate
echo ""
echo "------------------------------------"

echo "Check miner0 account"
curl -X POST -H 'content-type:application/json;' --data '{"address":"ppio1KgqNbxTiNqKyaahLFjSGGfK2WuJNR4HFb"}' http://127.0.0.1:8685/v1/user/accountstate
echo ""
echo "------------------------------------"

echo "Check miner1 account"
curl -X POST -H 'content-type:application/json;' --data '{"address":"ppio1QcM4YmKQ55q6NKFT7XR1ek21H3eYWE9zP"}' http://127.0.0.1:8685/v1/user/accountstate
echo ""
echo "------------------------------------"

echo "Check miner2 account"
curl -X POST -H 'content-type:application/json;' --data '{"address":"ppio1QkS9abTtBsSCFtMdBqqBFsJsBpcZuyc7q"}' http://127.0.0.1:8685/v1/user/accountstate
echo ""
echo "------------------------------------"

echo "Check miner3 account"
curl -X POST -H 'content-type:application/json;' --data '{"address":"ppio1awPPtYeyV1KsDLUuEHKHV9StKGycsg8f9"}' http://127.0.0.1:8685/v1/user/accountstate
echo ""
echo "------------------------------------"

echo "Check miner4 account"
curl -X POST -H 'content-type:application/json;' --data '{"address":"ppio1XHf9Pain1hoH11jfDc94K5Z1u4NeEpVdW"}' http://127.0.0.1:8685/v1/user/accountstate
echo ""
echo "------------------------------------"

echo ""
echo ""
echo ""
echo ""