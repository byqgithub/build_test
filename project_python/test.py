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


import threading


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@singleton
class Highlander(object):
    x = 100
    # Of course you can have any attributes or methods you like.


def worker():
    hl = Highlander()
    hl.x += 1
    print(hl)
    print(hl.x)


def main():
    threads = []
    for _ in range(50):
        t = threading.Thread(target=worker)
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()


if __name__ == '__main__':
    main()
