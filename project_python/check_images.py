# -*- coding: utf-8 -*-
# !/usr/bin/env python

import re
import sys
import time
import shlex
import getopt
import subprocess

usage = """
USAGE:
   --image:      image type: big: big ipes image; small: small ipes image
   --disk_num:   machine disk number
   --machine_id: machine id
   check_insatll_images.py --image=<big/small> --disk_num=<number> --machine_id=<id>

example:
   check_insatll_images.py --image=big --disk_num=12 --machine_id=XXXX
"""

env_check = [{"path": "/etc/ssh/sshd_config", "key": ["^MaxAuthTries\s+6", "^UseDNS\s+no"], "num": 2},
             {"path": "/etc/profile", "key": ["^TMOUT=300"], "num": 1},
             {"path": "/var/spool/cron/root",
              "key": ["^\*/30\s+\*\s+\*\s+\*\s+\*\s+/usr/sbin/ntpdate\s+asia.pool.ntp.org"],
              "num": 1},
             {"path": "/root/.bashrc", "key": ["^export\s+LANG=en_US.UTF-8"], "num": 1},
             {"path": "/etc/locale.conf", "key": ["^LANG=\"en_US.UTF-8\""], "num": 1},
             {"path": "/etc/rc.local", "key": ["^ulimit\s+-SHn\s+102400"], "num": 1},
             {"path": "/etc/security/limits.conf",
              "key": ["^\*\s+soft\s+nofile\s+102400", "^\*\s+hard\s+nofile\s+102400"],
              "num": 2},
             {"path": "/etc/sysctl.conf", "key": ["^kernel.*", "^net.core.*", "^net.ipv4.*"], "num": 10}]

disk_mount_command = "df -h |grep -E \"ssd|data\""
uuid_command = "cat /etc/fstab | grep UUID"
blkid_command = "blkid"
"/opt/soft/ipes/bin/ipes start"
"ps aux | grep \"ipes\|css\|dcache\" | grep -v grep"
"ps aux | grep \"ipes\" | grep -v grep"
"cat /opt/soft/dcache/deviceid"
"cat /etc/machine-id"
"docker ps"
"systemctl status %s |grep Active"


def exec_shell(command, shell=True):
    """ Exec shell cmd

    Args:
        command:
        shell:
        timeout:

    Return:
    Except:
    """
    command = "%s ; exit 0" % command
    print("cmd: %s" % command)
    if not shell:
        command = shlex.split(command)
    try:
        result = subprocess.check_output(command, shell=shell, stderr=subprocess.STDOUT).decode('utf-8')
        print("result: %s" % result)
        return result
    except subprocess.CalledProcessError as e:
        print_error("[ERROR] Execute shell command err: %s" % e)
        return ""


def print_ok(info):
    """ print successful info """
    print("\033[1;32m %s \033[0m" % info)


def print_error(info):
    """ print error """
    print("\033[1;31m %s \033[0m" % info)


def check_env_result():
    """ check env """
    print("----- Start check env -----")
    check_result = True
    for check_point in env_check:
        with open(check_point["path"]) as f_object:
            num = 0  # 指定文件中, 关键字出现的次数
            for line in f_object:
                for rule in check_point["key"]:
                    result = re.search(rule, line.strip())
                    if result is not None:
                        num += 1
                        print("Check file(%s) include info %s" % (check_point["path"], result.group()))

            # print("File(%s) include key number: %s" % (check_point["path"], num))
            if num < check_point["num"]:
                check_result = False
                print_error("Check file(%s) do not include info %s" % (check_point["path"], check_point["key"]))

    if check_result:
        print_ok("Check env result pass")
    else:
        print_error("[Error] Check env result error")

    print("----- End check env -----\n")
    return check_result


def check_disk_mount(num):
    """ Check disk mount """
    result = True
    print("----- Start check disk mount -----")
    disk_info = exec_shell("df -h |grep -E \"ssd|data\"")
    disk_used_info = disk_info.splitlines()
    for info in disk_used_info:
        usage_rate = re.search(".*(?P<rate>\d+)%.*", info)
        try:
            if not usage_rate or float(usage_rate.groups()[0]) > 1.0:
                result &= False
        except Exception as e:
            result &= False
            print_error("[Exception] %s" % e)

    result &= False if len(disk_used_info) != num else True

    if result:
        print_ok("Check disk mount pass")
    else:
        print_error("[Error] Check disk mount error")

    print("----- End check disk mount -----\n")
    return result


def check_disk_uuid(num):
    """ check disk uuid """
    result = True
    print("----- Start check disk uuid -----")
    fstab_info = exec_shell("cat /etc/fstab | grep UUID")
    blkid_info = exec_shell("blkid")

    fstab_rule = "^UUID=\"(?P<uuid>.+)\".*"
    blkid_rule = "^/dev.*UUID=\"(?P<uuid>.+)\".*TYPE.*"
    fstab_uuid = list()
    blkid_uuid = list()
    fstab_lines = fstab_info.splitlines()
    for info in fstab_lines:
        r = re.search(fstab_rule, info)
        fstab_uuid.append(r.groups()[0]) if r else None

    blkid_lines = blkid_info.splitlines()
    for info in blkid_lines:
        r = re.search(blkid_rule, info)
        blkid_uuid.append(r.groups()[0]) if r else None

    if len(fstab_uuid) > len(blkid_uuid) or len(fstab_uuid) != num:
        result = False
    else:
        for uuid in fstab_uuid:
            print("UUID: %s " % uuid)
            if uuid not in blkid_uuid:
                result = False

    if result:
        print_ok("Check disk uuid pass")
    else:
        print_error("[Error] Check disk uuid error")

    print("----- End check disk uuid -----\n")
    return result


def check_disk_result(disk_num):
    """ check disk result """
    return check_disk_mount(disk_num) & check_disk_uuid(disk_num)


def check_ipes_services(image_type):
    """ check ipes service """
    print("----- Start check ipes services -----")
    result = False
    if "big" in image_type:
        command = "ps aux | grep \"ipes\|css\|dcache\" | grep -v grep"
        services_name = ["ipes_check", "ipes start", "kcp", "ipes-agent", "ipes-manager", "ipes-hub", "dcache",
                         "ipes-store", "css"]
    else:
        command = "ps aux | grep \"ipes\" | grep -v color"
        services_name = ["ipes"]
    exec_shell("/opt/soft/ipes/bin/ipes start")
    index = 0
    for i in range(10):
        time.sleep(5)
        ps_info = exec_shell(command).splitlines()
        for count in range(len(services_name)):
            if count + index >= len(services_name):
                print_ok("All ipes services check completely")
                result = True  # all services running
                break  # count + index can not greater length of list, otherwise list index out of range

            name = services_name[count + index]
            for process in ps_info:
                if name in process:
                    print_ok("Ipes service: %s running" % name)
                    break  # if service running, break ps_info list loop
            else:
                index = count + index  # redefine index
                break  # if one service no running, break services_name list loop
        else:
            result = True  # all services running
            break

        if result:
            break  # all services running, exit check
    else:
        print_error("Ipes services: %s no running" % services_name[index:] if index < len(services_name) else "")

    device_id = exec_shell("cat /opt/soft/dcache/deviceid")
    result &= True if device_id else False
    if result:
        print_ok("Ipes device id is exist")
    else:
        print_error("[Error] Ipes device id is not exist")

    print("----- End check ipes services -----\n")
    return result


def check_qr_code(qr_code):
    """ Check machine id and qr code """
    print("----- Start check qr code -----")
    result = False
    machine_id = str(exec_shell("cat /etc/machine-id")).strip()
    print(machine_id)
    print(qr_code)
    if machine_id == qr_code:
        result = True
    if result:
        print_ok("Machine id == qr code")
    else:
        print_error("[Error] Machine id != qr code")
    print("----- End check qr code -----\n")
    return result


def check_docker_env():
    """ Check docker env """
    print("----- Start check docker env -----")
    result = False
    if exec_shell("docker ps"):
        print_ok("Docker installed")
        result = True
    else:
        print_error("[Error] Docker not installed")
    print("----- End check docker env -----\n")
    return result


def check_daemon_process():
    """ Check PI daemon process status """
    print("----- Start check daemon process env -----")
    result = True
    process_name = ["master", "telegraf", "docker"]
    for name in process_name:
        status = exec_shell("systemctl status %s |grep Active" % name)
        if "running" in status:
            print_ok("Service %s is running" % name)
        else:
            result &= False
            print_error("Service %s is inactive" % name)
    print("----- End check daemon process env -----\n")
    return result


def parse_argv(argv):
    """ parse script parameters """
    images = machine_id = str()
    num = 0
    try:
        opts, args = getopt.getopt(argv, "hi:n:m:", ["image=", "disk_num=", "machine_id=", "help"])
        if len(opts) < 3:
            print(usage)
            sys.exit(2)
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print(usage)
            sys.exit(2)
        elif opt in ("-i", "--image"):
            if not arg or arg not in ["big", "small"]:
                print_error("Image type error")
                sys.exit(2)
            else:
                images = arg
                print("Image type: %s" % images)
        elif opt in ("-n", "--disk_num"):
            if not arg:
                print_error("Disk number is NULL")
                sys.exit(2)
            else:
                num = int(arg)
                print("Disk number: %s" % num)
        elif opt in ("-m", "--machine_id"):
            if not arg:
                print_error("Machine id is NULL")
                sys.exit(2)
            else:
                machine_id = arg
                print("Machine id: %s" % machine_id)

    return images, num, machine_id


def main(argv):
    """  """
    images, num, machine_id = parse_argv(argv)
    result = check_env_result()
    if "big" in images:
        result &= check_disk_result(num)
        result &= check_ipes_services(images)
    result &= check_qr_code(machine_id)
    # result &= check_docker_env()
    result &= check_daemon_process()
    if result:
        print_ok("Image check pass")
    else:
        print_error("Image check failed")


if __name__ == "__main__":
    main(sys.argv[1:])
