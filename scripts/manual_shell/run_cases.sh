#!/bin/bash

cd $GOPATH/src/github.com/PPIO/go-ppio/service/ppio
file_path=/tmp/ppio_$(date "+%Y-%m-%d_%H-%M-%S")
echo $file_path
mkdir -p $file_path

date "+%Y-%m-%d_%H-%M-%S"

result=0
go test -v -run TestObjectPutSegment1Piece1Copy1Miner1 > $file_path/TestObjectPutSegment1Piece1Copy1Miner1.log
if [ $? -ne 0 ]
then
    result=1
    echo "TestObjectPutSegment1Piece1Copy1Miner1 Failed"
fi

go test -v -run TestObjectPutSegment1Piece2Copy1Miner1 > $file_path/TestObjectPutSegment1Piece2Copy1Miner1.log
if [ $? -ne 0 ]
then
    result=1
    echo "TestObjectPutSegment1Piece2Copy1Miner1 Failed"
fi

go test -v -run TestObjectPutSegment1PieceXCopy1Miner1_16M > $file_path/TestObjectPutSegment1PieceXCopy1Miner1_16M.log
if [ $? -ne 0 ]
then
    result=1
    echo "TestObjectPutSegment1PieceXCopy1Miner1_16M Failed"
fi

go test -v -run TestObjectPutSegment1Piece1Copy3Miner3 > $file_path/TestObjectPutSegment1Piece1Copy3Miner3.log
if [ $? -ne 0 ]
then
    result=1
    echo "TestObjectPutSegment1Piece1Copy3Miner3 Failed"
fi

go test -v -run TestObjectPutSegment3PieceXCopy3Miner3_33M > $file_path/TestObjectPutSegment3PieceXCopy3Miner3_33M.log
if [ $? -ne 0 ]
then
    result=1
    echo "TestObjectPutSegment3PieceXCopy3Miner3_33M Failed"
fi

go test -v -run TestObjectPutSimutaneously > $file_path/TestObjectPutSimutaneously.log
if [ $? -ne 0 ]
then
    result=1
    echo "TestObjectPutSimutaneously Failed"
fi

go test -v -run TestObjectGet > $file_path/TestObjectGet.log
if [ $? -ne 0 ]
then
    result=1
    echo "TestObjectGet Failed"
fi

go test -v -run TestObjectRenew > $file_path/TestObjectRenew.log
if [ $? -ne 0 ]
then
    result=1
    echo "TestObjectRenew Failed"
fi

go test -v -run TestObjectCopy > $file_path/TestObjectCopy.log
if [ $? -ne 0 ]
then
    result=1
    echo "TestObjectCopy Failed"
fi

#go test -v -run TestObjectUpdateAcl > $file_path/TestObjectUpdateAcl.log

go test -v -run TestMetadataPutAndGet > $file_path/TestMetadataPutAndGet.log
if [ $? -ne 0 ]
then
    result=1
    echo "TestMetadataPutAndGet Failed"
fi

go test -v -run TestMinerStroageTask > $file_path/TestMinerStroageTask.log
if [ $? -ne 0 ]
then
    result=1
    echo "TestMinerStroageTask Failed"
fi

go test -v -run TestMinerRescheduleTask > $file_path/TestMinerRescheduleTask.log
if [ $? -ne 0 ]
then
    result=1
    echo "TestMinerRescheduleTask Failed"
fi

go test -v -run TestMinerRetrievalTask > $file_path/TestMinerRetrievalTask.log
if [ $? -ne 0 ]
then
    result=1
    echo "TestMinerRetrievalTask Failed"
fi

go test -v -run TestObjectActionsWithCPool > $file_path/TestObjectActionsWithCPool.log
if [ $? -ne 0 ]
then
    result=1
    echo "TestObjectActionsWithCPool Failed"
fi

go test -v -run TestMetadataActionsWithCPool > $file_path/TestMetadataActionsWithCPool.log
if [ $? -ne 0 ]
then
    result=1
    echo "TestMetadataActionsWithCPool Failed"
fi

date "+%Y-%m-%d_%H-%M-%S"
exit result

