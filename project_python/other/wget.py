# -*- coding: utf-8 -*-

import os
import sys
import time
import math
import shlex
import random
import platform
from subprocess import check_output, STDOUT

proxy_dict = {
    "luminati_res": {"American": {"proxy": "zproxy.lum-superproxy.io:22225",
                                  "user": "lum-customer-humiao-zone-residential2-route_err-block-country-us",
                                  "password": "d312622131b6"},
                     # "Turkey":   {"proxy": "zproxy.lum-superproxy.io:22225",
                     #              "user": "lum-customer-humiao-zone-residential2-route_err-block-country-tr",
                     #              "password": "d312622131b6"},
                     # "Germany":  {"proxy": "zproxy.lum-superproxy.io:22225",
                     #              "user": "lum-customer-humiao-zone-residential2-route_err-block-country-de",
                     #              "password": "d312622131b6"},
                     # "HongKong": {"proxy": "zproxy.lum-superproxy.io:22225",
                     #              "user": "lum-customer-humiao-zone-residential2-route_err-block-country-hk",
                     #              "password": "d312622131b6"},
                     # "Iceland":  {"proxy": "zproxy.lum-superproxy.io:22225",
                     #              "user": "lum-customer-humiao-zone-residential2-route_err-block-country-is",
                     #              "password": "d312622131b6"},
                     # "Netherlands": {"proxy": "zproxy.lum-superproxy.io:22225",
                     #                 "user": "lum-customer-humiao-zone-residential2-route_err-block-country-nl",
                     #                 "password": "d312622131b6"},
                      },
    # "luminati_mobile": {"American": {"proxy": "zproxy.lum-superproxy.io:22225",
    #                               "user": "lum-customer-humiao-zone-mobile-route_err-block-country-us-mobile",
    #                               "password": "y3tvza2uyqml"},
    #                  "Turkey":   {"proxy": "zproxy.lum-superproxy.io:22225",
    #                               "user": "lum-customer-humiao-zone-mobile-route_err-block-country-tr-mobile",
    #                               "password": "y3tvza2uyqml"},
    #                  "Germany":  {"proxy": "zproxy.lum-superproxy.io:22225",
    #                               "user": "lum-customer-humiao-zone-mobile-route_err-block-country-de-mobile",
    #                               "password": "y3tvza2uyqml"},
    #                  "HongKong": {"proxy": "zproxy.lum-superproxy.io:22225",
    #                               "user": "lum-customer-humiao-zone-mobile-route_err-block-country-hk-mobile",
    #                               "password": "y3tvza2uyqml"},
    #                  "Iceland":  {"proxy": "zproxy.lum-superproxy.io:22225",
    #                               "user": "lum-customer-humiao-zone-mobile-route_err-block-country-is-mobile",
    #                               "password": "y3tvza2uyqml"},
    #                  "Netherlands": {"proxy": "zproxy.lum-superproxy.io:22225",
    #                                  "user": "lum-customer-humiao-zone-mobile-route_err-block-country-nl-mobile",
    #                                  "password": "y3tvza2uyqml"},
    #                  },
    "expressVPN": {"American": {"location": "USA - Los Angeles - 2"},
                   #  "Turkey":   {"location": "Turkey"},
                   #  "Germany":  {"location": "Germany - Frankfurt - 1"},
                   # "HongKong": {"location": "Hong Kong - 2"},
                   #  "Iceland":  {"location": "Iceland"},
                   #  "Netherlands": {"location": "Netherlands - Amsterdam"},
                   }
}

size = 50 * 1024
command = {"expressVPN": "wget --progress=bar \"http://vpn-tests.s3-us-west-2.amazonaws.com/ok.txt?from_region=%s&vpn=%s&vpn_region=%s&timestamp=%s\" -O %s 2>&1",
           "other": "wget -e use_proxy=yes -e http_proxy=%s --proxy-user %s --proxy-password %s --progress=bar \"http://vpn-tests.s3-us-west-2.amazonaws.com/ok.txt?from_region=%s&vpn=%s&vpn_region=%s&timestamp=%s\" -O %s 2>&1"}
# command = "wget -e use_proxy=yes -e http_proxy=%s --proxy-user %s --proxy-password %s --progress=bar \"http://vpn-tests.s3-us-west-2.amazonaws.com/ok.txt?from_region=%s&vpn=%s&vpn_region=%s&timestamp=%s\" -O %s 2>&1"


def gen_name(label):
    return "{}-{}".format(label, "".join(random.sample("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRETUVWXYZ",16)))


def get_file(command_dict, region):
    outfile_path = ""
    for proxy_key in proxy_dict:
        for zone in proxy_dict[proxy_key]:
            print("Start download")
            if "expressVPN" in proxy_key:
                location = proxy_dict[proxy_key][zone].get("location")
            else:
                proxy = proxy_dict[proxy_key][zone].get("proxy")
                user = proxy_dict[proxy_key][zone].get("user")
                password = proxy_dict[proxy_key][zone].get("password")
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "%s_%s_record.log" % (proxy_key, zone))
            print("Outfile path: %s" % path)
            location = ""
            if not express_vps_connect_status(proxy_key, location):
                continue

            for i in range(1):
                start_time = 0
                end_time = 0
                for j in range(3):
                    start_time = time.time()
                    file_name = gen_name("%s_%s" % (proxy_key, zone))
                    if "expressVPN" not in proxy_key:
                        cmd = command_dict.get("other")
                        wget_cmd = cmd % (proxy, user, password, region, proxy_key, zone, start_time, file_name)
                    else:
                        cmd = command_dict.get("expressVPN")
                        wget_cmd = cmd % (region, proxy_key, zone, start_time, file_name)
                    print("wget command: %s" % wget_cmd)
                    with os.popen(wget_cmd) as p:
                        ret = p.read()
                        if "100%" in ret:
                            end_time = time.time()
                            outfile_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                        "%s_%s_%s_%s_record.log" % (region, proxy_key, zone, start_time))
                            write_file(outfile_path, ret)
                            break
                        else:
                            end_time = 0
                            print("wget file error, cmd: %s, time: %s" % (wget_cmd, start_time))
                else:
                    print("wget command error")
                if start_time and end_time:
                    duration = end_time - start_time
                    # speed = size / duration
                    avg_speed, std_speed = statistic(outfile_path)
                    text = "start time: %s; end time: %s; duration: %s; avg speed: %s KB/s;  std speed: %s\n\n"
                    content = text % (start_time, end_time, duration, avg_speed, std_speed)
                    write_file(path, content)

            if "expressVPN" in proxy_key:
                os.system("expressvpn disconnect")
                print("expressVPN disconnect")


def express_vps_connect_status(proxy_name, location):
    """  """
    for try_time in range(3):
        if "expressVPN" in proxy_name:
            os.system("expressvpn connect \"%s\"" % location)
            # time.sleep(5)
            try:
                with os.popen("expressvpn status") as p:
                    return_str = p.read()
                    print("express VPN status: %s" % return_str)
                    if location not in return_str:
                        print("expressVPN connect failed")
                        os.system("expressvpn disconnect")
                        print("expressVPN disconnect")
                        continue
                    else:
                        print("expressVPN connect successful")
                        return True
            except Exception as e:
                print("Check express vpn status error: %s" % e)
        else:
            modify_dns_config()
            return True

    return False


def get_ip():
    with os.popen("hostname -I") as p:
        output = p.read()
    return output


def modify_dns_config():
    """  """
    if "centos" in platform.platform():
        with open("/etc/resolv.conf", "r+") as f:
            config = f.read()
            if "8.8.8.8" not in config:
                f.write("nameserver 8.8.8.8")
                print("Modify dns config successful")
            else:
                print("Do not modify dns config")
    else:
        print("Do not modify dns config")


def write_file(path, content):
    """  """
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path, "a") as f:
        f.write(content)


def statistic(outfile):
    """  """
    avg_speed = 0
    std_speed = 0
    if os.path.exists(outfile):
        count = 0
        sum = 0
        speed_list = list()
        with open(outfile) as f:
            for line in f:
                if ".........." in line:
                    count += 1
                    if count <= 5:
                        print(line)
                        continue

                    try:
                        speed = float(line.split(" ")[-2][0:-1].strip())
                        if "M" in line.split(" ")[-2][-1]:
                            speed = 1024 * speed
                        elif "G" in line.split(" ")[-2][-1]:
                            speed = 1024 * 1024 * speed
                        elif "K" in line.split(" ")[-2][-1] or "k" in line.split(" ")[-2][-1]:
                            speed = speed
                        else:
                            print("Statistic error, don not have the speed unit, content: %s" % line)
                            continue
                        sum += speed
                        speed_list.append(speed)
                    except Exception as e:
                        print("Statistic exception %s" % e)

            if len(speed_list):
                avg_speed = sum / len(speed_list)
            for element in speed_list:
                std_speed += math.pow(element - avg_speed, 2)
            std_speed = math.sqrt(std_speed / len(speed_list))

    return avg_speed, std_speed


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Input region params")
        exit(1)
    else:
        region = sys.argv[1]
        get_file(command, region)
