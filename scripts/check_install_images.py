# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
import re
import shlex
import subprocess

env_check = [{"path": "/etc/ssh/sshd_config", "key": ["^MaxAuthTries\s+6", "^UseDNS\s+no"], "num": 2},
             {"path": "/etc/profile", "key": ["^TMOUT=300"], "num": 1},
             {"path": "/var/spool/cron/root",
              "key": ["^*/30\s+*\s+*\s+*\s+*\s+/usr/sbin/ntpdate\s+asia.pool.ntp.org"],
              "num": 1},
             {"path": "/root/.bashrc", "key": ["^export\s+LANG=en_US.UTF-8"], "num": 1},
             {"path": "/etc/locale.conf", "key": ["^LANG=\"en_US.UTF-8\""], "num": 1},
             {"path": "/etc/rc.local", "key": ["^ulimit\s+-SHn\s+102400"], "num": 1},
             {"path": "/etc/security/limits.conf",
              "key": ["^*\s+soft\s+nofile\s+102400", "^*\s+hard\s+nofile\s+102400"],
              "num": 2},
             {"path": "/etc/sysctl.conf", "key": ["^kernel.*", "^net.core.*", "^net.ipv4.*"], "num": 10}]


def exec_shell(command, shell=False, timeout=200):
    """ Exec shell cmd

    Args:
        command:
        shell:
        timeout:

    Return:
    Except:
    """
    print("cmd: %s" % command)
    if not shell:
        command = shlex.split(command)
    try:
        result = subprocess.check_output(command, shell, timeout=timeout, stderr=subprocess.STDOUT).decode('utf-8')
        # print("result: %s" % result)
        return result
    except subprocess.CalledProcessError as e:
        print("[ERROR] Execute shell command err: %s" % e)


def env_check_result():
    """ Env check """
    print("----- Start env check -----")
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

            print("File(%s) include key number: %s" % (check_point["path"], num))
            if num < check_point["num"]:
                check_result = False

    print("Env check result: %s" % check_result)
    print("----- End env check -----")
    return check_result


def disk_check_result():
    """ Disk check result """

