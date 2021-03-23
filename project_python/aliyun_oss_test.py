# -*- coding: utf-8 -*-

import os
import sys
import oss2

access_key_id = ""
access_key_secret = ""
bucket_name = "pi-miner"
painull_path = "tools/painull/v%s"


def upload_file(file, version):
    auth = oss2.Auth(access_key_id, access_key_secret)
    endpoint = "http://oss-cn-beijing.aliyuncs.com"
    bucket = oss2.Bucket(auth, endpoint, bucket_name)
    # info = bucket.get_bucket_info()

    oss_path = os.path.join(painull_path % version, os.path.basename(file))
    for i in range(5):
        try:
            bucket.put_object_from_file(oss_path, file)
        except Exception as e:
            print("Upload file error: %s" % e)
        else:
            print("Upload file completely")
            break


if __name__ == '__main__':
    if len(sys.argv) >= 3:
        file_version = sys.argv[1]
        file_name = sys.argv[2]
        print("Upload file: %s" % file_name)
        print("Upload file version: %s" % file_version)
        upload_file(file_name, file_version)
    else:
        print("Input parameter error")
