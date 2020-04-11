#!/usr/bin/env bash

GOPATH=$(go env GOPATH)
GOPPIOROOT=$(go env GOPATH)/src/github.com/PPIO
GOPPIO=$(go env GOPATH)/src/github.com/PPIO/go-ppio
GOPROTO=$(go env GOPATH)/src/github.com/PPIO/ppio-proto

COMMIT_ID=$(git log --oneline -n 1 | cut -d " " -f1)
GIT_BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)
GIT_COMMIT_COUNT=$(git rev-list --count ${GIT_BRANCH_NAME} -- )
GO_LD_FLGAS="-X main._BUILDVERSION_='${COMMIT_ID}' -X github.com/PPIO/go-ppio/service.BUILD_NUMBER=${GIT_COMMIT_COUNT} -X github.com/PPIO/go-ppio/service.BUILD_BRANCH_NAME=${GIT_BRANCH_NAME} -X github.com/PPIO/go-ppio/service.BUILD_COMMIT_ID=${COMMIT_ID}"

VERSION=0.0.0

BUILD_TIME=$(date +"%Y-%m-%d_%H-%M-%S")

cd ${GOPPIO}/cmd/pcdn
rm -rf pcdn.exe
env CGO_ENABLED=1 GOOS=windows GOARCH=amd64  CC="x86_64-w64-mingw32-gcc" go build -ldflags "${GO_LD_FLGAS}"
cd -
