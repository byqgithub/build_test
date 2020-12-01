# -*- coding: utf-8 -*-

import os
import re
import sys
import time
import hmac
import hashlib
import base64
from urllib import parse
import requests

dingding_url = "https://oapi.dingtalk.com/robot/send?access_token=f4389c51620e92f2f28467f1b172084210a59ec03b007419f842e883d1520e1b"
# dingding_url = "https://oapi.dingtalk.com/robot/send?access_token=bcffddf3118914e15e4eabb14a317368e607143a1edb055286a97eddfd5b55c1"  # test url
secret = ""
# secret = "SECff417245dcbedefc7d66bdc9d64b3f97083653757fb91c30b8273759862c7fe4"  # test secret
message_text = {"msgtype": "text", "text": {"content": "Jenkins"}, "at": {"isAtAll": False}}
message_markdown = {"msgtype": "markdown", "markdown": {"title": "", "text": ""}, "at": {"isAtAll": False}}
auto_report = "artifact/go/src/github.com/PPIO/pi-miner/net-config/pairat/tools/paicheck_result.txt"


def url_sign():
    """ url sign with secret """
    #timestamp = round(time.time() * 1000)
    #secret_enc = bytes(secret, 'utf-8')
    #string_to_sign = '{}\n{}'.format(timestamp, secret)
    #string_to_sign_enc = bytes(string_to_sign, 'utf-8')
    #hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    #sign = parse.quote_plus(base64.b64encode(hmac_code))
    #url_signed = "%s&timestamp=%s&sign=%s" % (dingding_url, timestamp, sign)
    return dingding_url #url_signed


def statistic_result(report_url):
    """ Statistic report data """
    auth = ("core-auto-guest", "pplive123")
    result_dict = {"uptime": 0, "network": 0, "iptables": 0, "netout": 0, "netin": 0, "dns": 0, "cpu": 0, "wa": 0, "si": 0, "mem": 0, "sdisk": 0, "telgf": 0, "proxy": 0, "dcache": 0, "yf": 0, "ws": 0, "ks": 0, "happ": 0, "baidu": 0, "kcm": 0, "kc": 0, "no_result": 0}
    total = 0
    err_mark = ["WARN", "WARDK", "WARPS", "WARUR", "ERR", "ERRCF", "ERRSP"]
    result = requests.get(url=report_url, auth=auth, verify=False)
    if result.text:
        content = result.text.split("\n")
        for line in content[1:]:
            if not line:
                continue

            total += 1
            parsing = re.search("(?P<machineid>\w+)\s+(?P<uptime>\w+)\s+(?P<network>\w+)\s+(?P<iptables>\w+)\s+(?P<netout>\w+)\s+(?P<netin>\w+)\s+(?P<dns>\w+)\s+(?P<cpu>.*?)\s+(?P<wa>.*?)\s+(?P<si>.*?)\s+(?P<mem>.*?)\s+(?P<sdisk>.*?)\s+(?P<telgf>\w+)\s+(?P<proxy>\w+)\s+(?P<dcache>\w+)\s+(?P<yf>\w+)\s+(?P<ws>\w+)\s+(?P<ks>\w+)\s+(?P<happ>\w+)\s+(?P<baidu>\w+)\s+(?P<kcm>\w+)\s+(?P<kc>\w+)", line)
            if parsing is None:
                result_dict["no_result"] += 1
                print("no_result: %s" % line)
                continue

            for key in parsing.groupdict():
                if key in "machineid":
                    continue
                if parsing.groupdict()[key] in err_mark:
                    result_dict[key] += 1
    return result_dict, total


def markdown_content(project, job, report):
    """ test result markdown """
    result_dict, total = statistic_result(report)
    message_markdown["markdown"]["title"] = "Jenkins build result"
    message_markdown["markdown"]["text"] = "#### Jenkins project: %s result \n\n" % project + \
                                           "> [Job address](%s) \n\n" % job + \
                                           "> [Report address](%s) \n\n" % report + \
                                           "> Machine amount: %s \n\n" % total + \
                                           "> Err statistic: \n\n"

    for key in result_dict:
        message_markdown["markdown"]["text"] += "> %s = %s \n\n" % (key, result_dict.get(key))
    return message_markdown


def send_message(url, content):
    """ Send message to dingding """
    if not isinstance(content, dict):
        message_text["text"]["content"] = "Null"  # text 类型 message, content 为空, 消息无法发送到钉钉, 用于拦截无效消息
        message = message_text
    else:
        message = content
    print(message)
    for i in range(3):
        try:
            res = requests.post(url, json=message, timeout=30)
            print(message)
            response = res.json()
            if isinstance(response, dict):
                if "ok" in response.get("errmsg", ""):
                    print("Jenkins message send to dingding")
                    break
                else:
                    print("[Error] Jenkins can not message send to dingding, %s" % response.get("errmsg", ""))
        except Exception as e:
            print("[Error] Jenkins can not message send to dingding, Exception: %s" % e)


if "__main__" == __name__:
    project_name = os.environ.get("JOB_NAME", "Can not get project name from jenkins")
    job_url = os.environ.get("JOB_URL", "http://47.111.16.174:8899/")
    report_url = os.environ.get("BUILD_URL") + auto_report if os.environ.get("BUILD_URL", "") else "NULL"

    server_url = url_sign()
    content_dict = markdown_content(project_name, job_url, report_url)
    send_message(server_url, content_dict)
