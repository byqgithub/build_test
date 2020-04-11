# -*- coding: utf-8 -*-

import os
import hashlib
import requests
from requests.exceptions import RequestException, MissingSchema, Timeout


def read_chunks(obj, size):
    """  """
    obj.seek(0)
    chunk = obj.read(size)
    while chunk:
        # chunk = chunk.encode("utf-8")
        yield chunk
        chunk = obj.read(size)
    else:
        obj.seek(0)


def calc_file_md5(file_path):
    """ Calculation file hash use md5 """
    hash_md5 = str()
    method = hashlib.md5()
    if not os.path.exists(file_path):
        return hash_md5

    with open(file_path, 'rb') as f:
        for chunk in read_chunks(f, 1024 * 1024):
            method.update(chunk)
    return method.hexdigest()


def download_file(url, file_path, response, chunk_size=65535):
    """ Write download content into file
    Args:
        url:          url param
        file_path:    file path
        chunk_size:   file chunk size
        response:     http response instance
    Return:
        True:  download file successfully
        False: download file failed
    """
    try:
        downloaded = 0
        with open(file_path, "ab") as fd:
            for chunk in response.iter_content(chunk_size):
                fd.write(chunk)
                downloaded += len(chunk)
                print("{} bytes downloaded.".format(downloaded))
        print("%s download complete." % file_path)
        result = True
    except RequestException as e:
        print("[Error] Request url:%s; error reason %s" % (url.get("download_url", ""), e))
        os.remove(file_path) if os.path.exists(file_path) else ""
        result = False
    return result


def download_url(url, storage_path):
    try:
        with requests.get(url, stream=True, timeout=15, allow_redirects=False) as res:
            file_path = os.path.join(storage_path, url.rpartition("/")[-1])
            download_file(url, file_path, res)
    except MissingSchema:
        print("[Error] Invalid URL: %s" % url)
    except RequestException as e:
        print("[Error] Request url:%s; error reason %s" % (url, e))


def hls_download(m3us_file, url_header=""):
    """ hls download """
    md5 = calc_file_md5(m3us_file)
    hls_download_dir = os.path.join(os.path.dirname(m3us_file), md5)
    os.makedirs(hls_download_dir, exist_ok=True)
    with open(m3us_file) as f:
        for line in f.readlines():
            if ".ts" in line:
                url = url_header + "/" + line.strip()
                print("Hls piece url: %s" % url)
                download_url(url, hls_download_dir)


if __name__ == "__main__":
    hls_download(r"D:\test_log\pcdn_win\hls_resource\57c7f47ee3464336a39974bb25407d0c-5a4b08deb359074d220237b2e9ad53d3-ld.m3u8",
                 "http://videoplay.3453k.cn/0acdefa980ae4179bc0d4055d9c283f1")
