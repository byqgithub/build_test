# -*- coding: utf-8 -*-

import os
import time
import logging
import difflib
import requests
import datetime
from requests.exceptions import RequestException, MissingSchema, Timeout

g_logger = None
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
url_list = {#"hua_jun": {"download_url": "http://forspeed.onlinedown.net/down/QQ9.1.0.24712.exe",
                        # "referer": "http://www.onlinedown.net/soft/1424.htm",
                      #   "name": "QQ_PC"},
            # "xitongtiandi": {"download_url": "https://dldir1.qq.com/qqfile/qq/QQ9.0.4/23766/QQ9.0.4.exe",
            #                  "name": "QQ_PC"},
            # "skycn": {"download_url": "http://download.skycn.com/hao123-soft-online-bcs/soft/2017_02_22_QQ8.9.exe",
            #           "name": "QQ_PC"},
            # "duote": {"download_url": "http://soft.duote.com.cn/qq_9.1.0.24712.exe",
            #           "name": "QQ_PC"},
            # "mydown.yesky": {"download_url": "http://mydown.yesky.com/xzdown/364003?isxzq=0",
            #                  "name": "QQ_PC"},
            # "xiazaiba": {"download_url": "https://xiazai.xiazaiba.com/Soft/Q/QQ_9.1.0.24712_XiaZaiBa.zip",
            #              "name": "QQ_PC"},
            # "crsky": {"download_url": "http://9.gddx.crsky.com/soft/201901/QQ-v9.0.9.24413Trial.zip",
            #           "name": "QQ_PC"},
            # "pc6": {"download_url": "http://8dx.pc6.com/wwb6/QQ91024712.zip",
            #         "name": "QQ_PC"},
            # "33lc": {"download_url": "https://dldir1.qq.com/qqfile/qq/QQ9.0.6/24044/QQ9.0.6.24044.exe",
            #          "name": "QQ_PC"},
            # "52z": {"download_url": "http://dx60.91tzy.com:8070/QQ.exe",
            #         "name": "QQ_PC"},
            # "jyrd": {"download_url": "https://down10.jyrd.com/2010/QQ_lsb_3987.com.rar",
            #          "name": "QQ_PC"},
            # "cncrk": {"download_url": "http://xz.cncrk.com:8080/soft/keygen/QQ2019.rar",
            #           "referer": "http://www.cncrk.com/downinfo/260019.html",
            #           "name": "QQ_PC"},
            # "uzzf": {"download_url": "http://u10.innerpeer.com/pc/txqq.zip",
            #          "name": "QQ_PC"},
            # "soft.hao123": {"download_url": "http://softdown1.hao123.com/hao123-soft-online-bcs/soft/2017_02_22_QQ8.9.exe",
            #                 "name": "QQ_PC"},
            # "cr173": {"download_url": "http://xzf.jc9559.com/QQ9.1.0.24712.zip",
            #           "name": "QQ_PC"},
            # "qqtn": {"download_url": "http://dx11.dkgcw.com/qq910.zip",
            #          "name": "QQ_PC"},
            # "downza": {"download_url": "http://www.downza.cn/download/27540?module=soft&id=27540&token=b36e6b6b1bd9bb2dbc3ab4a8ab8a81bc&isxzq=0",
            #            "name": "QQ_PC"},
            # "greenxf": {"download_url": "http://gd2.greenxf.com:8099/联络聊天/QQ软件区/QQkgzd423(www.greenxf.com).rar",
            #             "name": "QQ_PC"},
            # "jz5u": {"download_url": "http://fzyd.jz5u.com:7011/soft-2011-08/Baofeng5youhuaban.rar",
            #          "name": "bao_feng"},
            # "dl.pconline": {"download_url": "http://dlc2.pconline.com.cn/filedown_359460_12708871/SM8nRPBw/QQ9.1.0.24707.exe",
            #                 "name": "QQ_PC"},
            # "pcsoft": {"download_url": "http://forspeed.pcsoft.com.cn/download/pc/QQ9.0.6.exe",
            #            "name": "QQ_PC"},
            # "wmzhe": {"download_url": "http://dl-t1.wmzhe.com/1/1415/QQ9.1.0.24707.exe",
            #           "name": "QQ_PC"},
            # "liqucn": {"download_url": "https://count.liqucn.com/d.php?id=799166",
            #            "name": "QQ_PC"},
            # "bkill": {"download_url": "http://dx.nongpin123.com:806/bugai/Baofengyinying_bkill.com.zip",
            #           "name": "bao_feng"},
            # "ddooo": {"download_url": "http://gd.ddooo.com:8081/uuauth/qq2015zsb_61449.rar?2537de0141eb160fc10f10040326db9f.rar",
            #           "name": "QQ_PC"},
            # "xiazai.zol": {"download_url": "http://down10.zol.com.cn/liaotian/QQ9.1.0.24712.exe",
            #                "name": "QQ_PC"},
            # "downxia": {"download_url": "http://sd.downxia.com/down/QTalkgf.rar",
            #             #"referer": "http://www.downxia.com/downinfo/6448.html",
            #             "cookie": "Hm_lvt_00526ff88a0f942f7aba7a59e0e7b53b=1554371058; vspublic=4e0e89a0ba5bbe7757e665df6c93d5cb; Hm_lpvt_00526ff88a0f942f7aba7a59e0e7b53b=1554791828",
            #             "name": "QQTalk"},
            #"downxia1": {"download_url": "http://forspeed.onlinedown.net/down/W.P.S.5559.20.2422.exe",
                        #"referer": "http://www.onlinedown.net/soft/295594.htm",
                        # "cookie": "Hm_lvt_1057fce5375b76705b65338cc0397720=1561552972; _ga=GA1.2.14362628.1561552973; _gid=GA1.2.74597064.1561552973; Qs_lvt_67987=1561552973; Hm_lpvt_1057fce5375b76705b65338cc0397720=1561554225; _gat=1; Qs_pv_67987=3630439863246662700%2C1923352322803352300%2C2093226224970546200%2C1576792773355124500%2C3848044187923644400",
                        #"name": "QQTalk"},
            # "newasp": {"download_url": "http://down-www.newasp.net/pcdown/soft/soft1/qq.exe",
            #            "name": "QQ_PC"},
            # "xz7": {"download_url": "http://gzy.funkg.com/soft/pcqq_xz7.com.zip",
            #         "name": "QQ_PC"},
            # "kddf": {"download_url": "https://1.kddf.com/xp2011/QQ5.4Trial_xp510.rar",
            #          "name": "QQ_PC"},
            # "ttrar": {"download_url": "http://pcdown.ttrar.com/small/qq2017_ttrar.exe",
            #           "name": "QQ_PC"},
            # "download.pchome": {"download_url": "https://dl-sh-ctc-2.pchome.net/0l/vk/QQ9.1.0.24712.zip",
            #                     "name": "QQ_PC"},
            # "orsoon": {"download_url": "http://d1.wlrjy.com:9876//网络工具/QQ　专区/drg0510/qq2017.rar",
            #            "": "https://www.wlrjy.com/Soft/23140.html",
            #            "name": "QQ_PC"},
            # "9553": {"download_url": "http://zj.9553.com/soft/QQ9.0.9_1xz.rar",
            #          "name": "QQ_PC"},
            # "xpgod": {"download_url": "http://psoft.xpgod.com:801/small/qq2019_xpgod-com.zip",
            #           "name": "QQ_PC"},
            # "7edown": {"download_url": "http://www.7edown.com/download.asp?id=40397&dp=1",
            #            "referer": "http://www.7edown.com/xiazai/40397.html",
            #            "name": "QQ_PC"},
            # "mt30": {"download_url": "http://wt.mt30.com/201712/QQ8.9.6.rar",
            #          "name": "QQ_PC"},
            # "rsdown": {"download_url": "http://d1.rsdown.cn/soft2/QQ2014 6.3.12382.0.zip",
            #            "name": "QQ_PC"},
            # "opdown": {"download_url": "http://down2.opdown.com:8081/opdown/QQ_opdown.com.zip",
            #            "name": "QQ_PC"},
            # "3322": {"download_url": "http://cnlt.jj55.com/txqq_1165.zip",
            #          "name": "QQ_PC"},
            # "121down": {"download_url": "http://down2.121down.com:8181/soft/QQTrial.rar",
            #             "name": "QQ_PC"},
            # "youxiaxiazai": {"download_url": "http://dianxin.youxia-down.671327.com:89/ziyuan/aruisibingdupojieban.apk",
            #                  "name": "a_rei_si_bing_du"},
            # "soft.jiegeng": {"download_url": "",
            #                  "name": "QQ_PC"},
            # "34ey": {"download_url": ""}
            "test": {"download_url": "http://192.168.50.207:8080/match_cookie_download/256M",
                     "cookie": "cookie=chrome",
                     "name": "cookie_file"}
            }

range_list = [(0, 1024 * 1024),
              (1 * 1024 * 1024 + 1, 20 * 1024 * 1024),
              (20 * 1024 * 1024 + 1, 40 * 1024 * 1024),
              (40 * 1024 * 1024 + 1, "end"),
              (0, "end")
              ]


def set_logger(timestamp, path="", category="log", clear_handler=True):
    """ Set logger system
    Args:
        timestamp:      log timestamp
        path:           log path
        category:       file content category
        clear_handler:  clear logger handler(True: clear; False: not clear)
    Return:
        logger instance
    """
    logger_name = 'range_download'
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    if clear_handler:
        for handler in logger.handlers:
            logger.removeHandler(handler)

    dir_name = "log" if "log" in category else "result"
    if path:
        log_path = os.path.join(path, dir_name, "%s_%s.log" % (dir_name, timestamp))
    else:
        log_path = os.path.join(os.getcwd(), dir_name, "%s_%s.log" % (dir_name, timestamp))

    if not os.path.exists(os.path.dirname(log_path)):
        os.makedirs(os.path.dirname(log_path))
        print('Create log dir: %s' % os.path.dirname(log_path))

    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    log_format = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
    data_format = "%a %d %b %Y %H:%M:%S"
    formatter = logging.Formatter(log_format, data_format)
    file_handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console)
    return logger


def file_size(filename):
    """ Get file size
    Args:
        filename: file path
    Return:
        file size
    """
    return os.stat(filename).st_size


def process_file_param(url, storage_path, download_range):
    """ Get file name and path
    Args:
        url:             url param
        storage_path:    storage root path
        download_range:  download range(type: tuple)
    Return:
        file name
        file abspath
        bytes range
    """
    if len(download_range):
        start = download_range[0]
        end = download_range[1]
    else:
        start = end = None

    filename = url.get("name", "No resource")
    bytes_range = None

    if start is None and end is None:
        filename = filename + "_" + "not_range"
    elif start == 0 and isinstance(end, str):
        filename = filename + "_" + "all_ranges"
    else:
        filename = filename + "_(" + str(start) + "-" + str(end) + ")"
    file_path = os.path.join(os.path.abspath(storage_path), filename)

    if start is not None and end is not None:
        bytes_range = 'bytes=%s-%s' % (start, end if not isinstance(end, str) else "")

    return filename, file_path, bytes_range


def is_download_file(file_path, size, re_download=False):
    """ If download file
    Args:
        file_path:   file path
        size:        file size
        re_download: re-download flag(True: re-download; False: don not download)
    Return:
        True:  download file
        False: don not download file
    """
    is_download = True
    if os.path.isfile(file_path):
        if file_size(file_path) == size:
            if re_download is False:
                g_logger.info("File already exists, do not re-download.")
                is_download = False
            else:
                os.remove(file_path)
                g_logger.info("File already exists, re-download.")
        else:
            os.remove(file_path)
            g_logger.info("File already exists, but size error, re-download.")
    else:
        g_logger.info("File not exists, download file.")

    return is_download


def download_file(url, file_path, chunk_size, response):
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
                g_logger.debug("{} bytes downloaded.".format(downloaded))
        g_logger.info("%s download complete." % file_path)
        result = True
    except RequestException as e:
        g_logger.error("[Error] Request url:%s; error reason %s" % (url.get("download_url", ""), e))
        os.remove(file_path) if os.path.exists(file_path) else ""
        result = False
    return result


def download(url, storage_path, range_tuple=tuple(), chunk_size=65535, re_download=False):
    """ Download file
    Args:
        url:           url param
        storage_path:  file storage path
        range_tuple:   http download range
        chunk_size:    file chunk size
        re_download:   re-download flag(True: re-download; False: don not download)
    Return:
        True:  download file successfully
        False: download file failed
    """
    filename, file_path, bytes_range = process_file_param(url, storage_path, range_tuple)

    # Update request header and cookies
    headers = dict()
    if bytes_range:
        headers['Range'] = bytes_range
    # headers["user-agent"] = user_agent
    headers["referer"] = url.get("referer", "")

    cookies = dict()
    if "cookie" in url.keys():
        for content in url.get("cookie").split(";"):
            key, value = content.strip().split("=")
            cookies[key] = value

    result = False
    g_logger.info("Download file %s to %s" % (filename, file_path))
    for i in range(3):
        try:
            with requests.get(url.get("download_url", ""),
                              headers=headers,
                              stream=True,
                              timeout=15,
                              cookies=cookies,
                              allow_redirects=False) as res:
                content_len = int(res.headers.get('content-length', 0))
                if is_download_file(file_path, content_len, re_download=re_download):
                    g_logger.debug("%s bytes to download." % content_len)

                    if res.status_code == 206:  # Check if server supports range feature, and works as expected.
                        # Content range is in format `bytes 327675-43968289/43968290`
                        content_range = res.headers.get('content-range')
                        g_logger.debug("Download request info: content-range %s" % content_range)
                        # If range error, it will return `bytes */43968290`.
                        if "*" not in content_range:
                            result = download_file(url, file_path, chunk_size, res)
                        else:
                            g_logger.error("[Error] %s file range download error" % filename)
                    elif res.status_code == 200:
                        g_logger.info("status code %s, can not partly download" % res.status_code)
                        result = download_file(url, file_path, chunk_size, res)
                        if res.headers.get('Location'):
                            url["download_url"] = res.headers.get('Location')
                            g_logger.info("Location url: %s" % res.headers.get('Location'))
                    elif res.status_code == 302 or res.status_code == 301:
                        url["download_url"] = res.headers.get('Location')
                        g_logger.info("Location url: %s" % res.headers.get('Location'))
                    elif res.status_code == 416:
                        g_logger.error("[Error] %s file download range error." % filename)
                    else:
                        g_logger.info("request status code: %s" % res.status_code)
                else:
                    result = True
            if result:
                break
        except MissingSchema:
            g_logger.error("[Error] Invalid URL: %s" % url.get("download_url", ""))
            break
        except RequestException as e:
            g_logger.error("[Error] Request url:%s; error reason %s" % (url.get("download_url", ""), e))
            os.remove(file_path) if os.path.exists(file_path) else ""
            time.sleep(60)

    return result


def download_range(url, storage_path, range_tuple=tuple(), chunk_size=65535, re_download=False):
    """ Download special part of file
    Args:
        url:           url param
        storage_path:  file storage path
        range_tuple:   http download range
        chunk_size:    file chunk size
        re_download:   re-download flag(True: re-download; False: don not download)
    Return:
        True:  download file successfully
        False: download file failed
    """
    return download(url, storage_path, range_tuple=range_tuple, chunk_size=chunk_size, re_download=re_download)


def download_not_range(url, storage_path, chunk_size=65535, re_download=False):
    """ Download all content of file
    Args:
        url:           url param
        storage_path:  file storage path
        chunk_size:    file chunk size
        re_download:   re-download flag(True: re-download; False: don not download)
    Return:
        True:  download file successfully
        False: download file failed
    """
    return download(url, storage_path, range_tuple=tuple(), chunk_size=chunk_size, re_download=re_download)


def get_file_range(file_name):
    """ Get file size range
    Args:
        file_name:   file name
    Return:
        start: file start byte
        size:  file size
    """
    start = 0
    size = -1
    file_range = file_name.partition('(')[-1].partition(")")[0].split("-")
    if len(file_range) == 2:
        start = int(file_range[0]) if len(file_range[0]) != 0 else 0
        size = (int(file_range[1]) - start + 1) if "end" not in file_range[1] else -1
    return start, size


def compare_file(path):
    """ Compare part fo files with full file
    Args:
        path:   file storage root path
    Return:
        True:  compare files successfully
        False: compare files failed
    """
    compare_result = True
    file_list = list()
    all_file_name = str()
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if "all" not in file_name:
                file_list.append(file_name)
            else:
                all_file_name = file_name

    if all_file_name:
        try:
            with open(os.path.join(path, all_file_name), errors="ignore") as all_file:
                for name in file_list:
                    start, size = get_file_range(name)
                    all_file.seek(start)
                    with open(os.path.join(path, name), errors="ignore") as f:
                        content_range = f.read()
                        content_part = all_file.read(len(content_range)).splitlines()
                        content_range = content_range.splitlines()
                        matcher = difflib.SequenceMatcher(None, content_range, content_part)
                        g_logger.debug("part len: %s; range len: %s" % (len(content_part), len(content_range)))
                        if round(matcher.ratio(), 3) == 1:
                            compare_result &= True
                        else:
                            compare_result &= False
                        g_logger.debug("File(part of %s and %s) compare result: %s" % (all_file_name,
                                                                                       name,
                                                                                       compare_result))
        except MemoryError as e:
            g_logger.error("File read error, %s" % e)
    else:
        g_logger.info("Compare files are incomplete.")

    return compare_result


def http_range_download(url_list, range_list, root_path, re_download=False):
    """ Download file and compare part fo files with full file
    Args:
        url_list:    url param
        range_list:  http download range
        root_path:   file storage root path
        re_download: re-download flag(True: re-download; False: don not download)
    Return:
        True:  download file and compare files successfully
        False: download file or compare files failed
    """
    current_time = datetime.datetime.now()
    timestamp = datetime.datetime.strftime(current_time, "%Y-%m-%d_%H-%M-%S")
    global g_logger
    g_logger = set_logger(timestamp, root_path, clear_handler=True)

    for key in url_list:
        result = True
        storage_path = os.path.join(root_path, key)
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)
        g_logger.info("Download website: %s" % key)
        for range_tuple in range_list:
            result &= download_range(url_list.get(key), storage_path, range_tuple, re_download=re_download)
        result &= download_not_range(url_list.get(key), storage_path, re_download=re_download)
        result &= compare_file(storage_path)
        g_logger.info("Website %s http range download result: %s" % (key, result))
        g_logger.info("\n\n\n\n")


if "__main__" == __name__:
    root_path = "D:\download\http_range_download\\test_data"
    http_range_download(url_list, range_list, root_path, re_download=False)
