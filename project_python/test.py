# import json
# import os
# import sys
#
# d = action_flow = {"action0": {'member': 'user0',
#                                'cpool': True,
#                                'action': 'PutObject',
#                                'fee': {'indexer': "PutObject",
#                                        'miners0': "PoST",
#                                        'verifier': 'PoST'},
#                                # 'refund': {'user0': "StorageContract",
#                                #            'miners0': 'StorageContract'},
#                                # 'reward': {'miners0': ["PoLC", "PoST"],
#                                #            'other': ["indexer", "verifier"]}
#                               },
#                    "action1": {'member': 'user0',
#                                'cpool': True,
#                                'action': 'RenewObject',
#                                'fee': {'indexer': "RenewObject",
#                                        'miners0': "PoST",
#                                        'verifier': 'PoST'},
#                                },
#                    "action2": {'member': 'user1',
#                                'cpool': True,
#                                'action': 'CopyObject',
#                                'fee': {'indexer': "CopyObject",
#                                        'miners1': "PoST",
#                                        'verifier': 'PoST'},
#                                },
#                    "action3": {'member': 'miners1',
#                                'cpool': False,
#                                'action': 'RequestScheduleTask',
#                                'fee': {'indexer': "RequestScheduleTask"},
#                                },
#                    "action4": {'member': 'user1',
#                                'cpool': True,
#                                'action': 'UpdateObjectAcl',
#                                'fee': {'indexer': "UpdateObjectAcl"},
#                                },
#                    "action5": {'member': 'user1',
#                                'cpool': False,
#                                'action': 'DeleteObject',
#                                'fee': {'indexer': "DeleteObject"}
#                                },
#                    "action6": {'member': 'user0',
#                                'cpool': True,
#                                'action': 'PutObject',
#                                'refund': {'user0': "1",
#                                           'miners0': '0'}
#                                },
#                    "action7": {'member': 'user1',
#                                'cpool': True,
#                                'action': 'PutObject',
#                                'refund': {'user1': "1",
#                                           'miners1': '0'},
#                                'reward': {'miners0': ["PoLC", "PoST"],
#                                           'miners1': ["PoLC", "PoST"],
#                                           'other': ["indexer", "verifier"]}
#                                }
#                    }
# print(json.dumps(action_flow))
# print(os.path.dirname(__file__))
#
#
# def test_test():
#     print(sys._getframe().f_code.co_name)
#
# # test_test()
#
# def cals(file):
#     """  """
#     total = 0
#     with open(file) as f:
#         for line in f:
#             total += float(line.strip())
#     print("%f" % total)
#
#
# if "__main__" == __name__:
#     #
#     s = int("2000000000000000000000000000000000000000000000000000000000000000000000000000")
#     print(s)
#     s = s + 1
#     print(s)
#     print(type(int("2000000000000000000000000000000000000000000000000000000000000000000000000000")))
#     s = 0
#     while True:
#         s = (s*s + 1)
#         print(s)


# import threading
#
#
# def singleton(cls):
#     _instance = {}
#
#     def _singleton(*args, **kargs):
#         if cls not in _instance:
#             _instance[cls] = cls(*args, **kargs)
#         return _instance[cls]
#
#     return _singleton
#
#
# @singleton
# class Highlander(object):
#     x = 100
#     # Of course you can have any attributes or methods you like.
#
#
# def worker():
#     hl = Highlander()
#     hl.x += 1
#     print(hl)
#     print(hl.x)
#
#
# def main():
#     threads = []
#     for _ in range(50):
#         t = threading.Thread(target=worker)
#         threads.append(t)
#
#     for t in threads:
#         t.start()
#
#     for t in threads:
#         t.join()
#
#
# if __name__ == '__main__':
#     main()
# import os
# import fcntl
#
#
# def single_instance_protection():
#     """ Daemon is single instance process, forbid multi instance running simultaneously """
#     pid_file = "/tmp/pid_file.pid"
#     try:
#         if os.path.exists(pid_file):
#             lockfile = open(pid_file, 'a+')
#             lockfile.write("1024")
#             lockfile.close()
#             lockfile = open(pid_file, 'r')
#             fcntl.lockf(lockfile.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
#             print("pid: %s" % lockfile.read())
#         else:
#             print("%s pid file is not exist" % pid_file)
#     except OSError as e:
#         print("Fork: can not open pid file")
#
#
# def read_file():
#     pid_file = "/tmp/pid_file.pid"
#     try:
#         with open(pid_file, "r") as f:
#             fcntl.lockf(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
#             print(f.read())
#     except OSError as e:
#         print("Open file %s error %s" % (pid_file, e))
#
#
# single_instance_protection()
import os
import time
import shlex
import subprocess


command = "netstat -s | awk '{if($2==\"segments\")a[$2$3$4]=$1}END{print a[\"segmentsretransmited\"]\"++\"a[\"segmentssendout\"]}'"


def exec_shell(command, shell=True, cwd=None, show_exception=False, debug=True):
    """ Exec shell cmd """
    command = "%s" % command
    print("cmd: %s" % command) if debug else ""
    if not shell:
        command = shlex.split(command)
    if cwd is None:
        cwd = os.path.abspath(os.path.dirname(__file__))
    try:
        result = subprocess.check_output(command, shell=shell, stderr=subprocess.STDOUT, cwd=cwd).decode('utf-8')
        print("result: %s" % result) if debug else ""
        return result
    except subprocess.CalledProcessError as e:
        print("Execute shell command err: %s" % e)
        return "EXCEPTION" if show_exception else ""


def print_time(msg):
    print("%s: %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) , msg))


if __name__ == '__main__':
    result = exec_shell(command, debug=False)
    pre_retran = float(result.split("++")[0])
    pre_send = float(result.split("++")[1])
    while True:
        time.sleep(5)
        result = exec_shell(command, debug=False)
        retran = float(result.split("++")[0])
        send = float(result.split("++")[1])
        print_time("pre retran %s, current retran %s" % (pre_retran, retran))
        print_time("pre send %s, current send %s" % (pre_send, send))
        if send >= pre_send and retran >= pre_retran:
            value = (retran - pre_retran) / (send - pre_send)
            print_time("TCP retransmission ratio %s" % value)
            pre_retran = retran
            pre_send = send
