# -*- coding: utf-8 -*-

import re
import os
import sys
import json
import getopt
from settlement_check.utile import g_logger
from settlement_check.constant import Constant
from settlement_check.settlement import Settlement
from settlement_check.account_analysis import ParseConsoleFile, ParseBillFile, ParseSyncAccountFile


action_flow = {"action0": {'member': 'user0',
                           'cpool': True,
                           'action': 'PutObject',
                           'fee': {'indexer': "PutObject",
                                   'miner0': "PoST",
                                   'verifier': 'PoST'},
                           # 'refund': {'user0': "StorageContract",
                           #            'miner0': 'StorageContract'},
                           # 'reward': {'miner0': ["PoLC", "PoST"],
                           #            'other': ["indexer", "verifier"]}
                           },
               "action1": {'member': 'user0',
                           'cpool': True,
                           'action': 'RenewObject',
                           'fee': {'indexer': "RenewObject",
                                   'miner0': "PoST",
                                   'verifier': 'PoST'},
                           },
               "action2": {'member': 'user1',
                           'cpool': True,
                           'action': 'CopyObject',
                           'fee': {'indexer': "CopyObject",
                                   'miner1': "PoST",
                                   'verifier': 'PoST'},
                           },
               "action3": {'member': 'miner1',
                           'cpool': False,
                           'action': 'RequestScheduleTask',
                           'fee': {'indexer': "RequestScheduleTask"},
                           },
               "action4": {'member': 'user1',
                           'cpool': True,
                           'action': 'UpdateObjectAcl',
                           'fee': {'indexer': "UpdateObjectAcl"},
                           },
               "action5": {'member': 'user1',
                           'cpool': False,
                           'action': 'DeleteObject',
                           'fee': {'indexer': "DeleteObject"}
                           },
               "action6": {'member': 'user0',
                           'cpool': True,
                           'action': 'PutObject',
                           'refund': {'user0': "1",
                                      'miner0': '0'}
                           },
               "action7": {'member': 'user1',
                           'cpool': True,
                           'action': 'PutObject',
                           'refund': {'user1': "1",
                                      'miner1': '0'},
                           'reward': {'miner0': ["PoLC", "PoST"],
                                      'miner1': ["PoLC", "PoST"],
                                      'other': ["indexer", "verifier"]}
                           }
               }


def compare_dict(obj_a, obj_b):
    """ Compare dict

    Args:
        obj_a: dict object a
        obj_b: dict object b

    Return:
        True:
        False:
    """
    obj_a_keys = sorted(obj_a.keys())
    obj_b_keys = sorted(obj_b.keys())
    if obj_a_keys != obj_b_keys:
        return False

    for key in obj_a:
        if str(obj_a[key]) != str(obj_b[key]):
            return False

    return True


def find_file_path(folder):
    g_logger.debug("\n\n\n\n")
    path_dict = dict().fromkeys(Constant.FILE_DICT.keys())
    for key in Constant.FILE_DICT:
        for root, dirs, files in os.walk(folder):
            for name in files:
                if re.search(Constant.FILE_DICT[key], name):
                    path_dict[key] = os.path.join(root, name)
                    g_logger.debug("%s path: %s" % (key, path_dict[key]))
    return path_dict


def parse_json_params(file_path):
    """ Parse json file, fetch params for settlement class

    Args:
        file_path: json file path

    Return:
        action_params: action flow params
        cal_params:    cal params for settlement
    """
    json_params = json.load(open(file_path))
    cal_params = json_params['cal']
    action_params = json_params['action']
    return action_params, cal_params


def bill_compare(raw_data, generate_data):
    compare_result = True
    for item in raw_data:
        for content in raw_data[item]:
            for obj in generate_data[item]:
                if compare_dict(content, obj):
                    break
            else:
                compare_result = False
                g_logger.error("[Result] Bill data diff, sourse data: %s," % content)
    if compare_result:
        g_logger.info("[Result] Bill data right")


def sync_account_compare(raw_data, generate_data):
    compare_result = True
    for item in raw_data:
        if compare_dict(raw_data[item], generate_data[item.lower()]):
            continue
        else:
            compare_result = False
            g_logger.error("[Result] Sync_account data diff, sourse data: %s, generate data: %s" % (
                raw_data[item],
                generate_data[item.lower()]))
    if compare_result:
        g_logger.info("[Result] Sync_account data right")


def account_total_compare(raw_data, generate_data):
    if not compare_dict(raw_data, generate_data):
        g_logger.error("[Result] CalcTotalChange diff, sourse data: %s, generate data: %s" % (raw_data, generate_data))
    else:
        g_logger.info("[Result] CalcTotalChange data right")


def account_compare(raw_data, generate_data):
    compare_result = True
    for member in generate_data:
        for time in generate_data[member]:
            for name in generate_data[member][time]:
                if str(raw_data[member][time][name]) != str(int(generate_data[member][time][name])):
                    compare_result = False
                    g_logger.error("[Result] Balance and locked data diff, sourse data: %s %s %s %s, generate info: %s %s %s %s" %
                                   (member, time, name, raw_data[member][time][name],
                                    member, time, name, generate_data[member][time][name]
                                    ))
    if compare_result:
        g_logger.info("[Result] Balance and locked data right")


def main(argv):
    """ Main """
    path = ''
    action_json_file = ''
    try:
        opts, args = getopt.getopt(argv, "hp:a:", ["path=", "action="])
    except getopt.GetoptError:
        print('main.py --path <file_path> --action <action_json_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py --path <file_path> --action <action_json_file>')
            sys.exit()
        elif opt in ("-p", "--path"):
            path = arg
        elif opt in ("-a", "--action"):
            action_json_file = arg
            if not os.path.exists(action_json_file):
                print('action json file do not exit')

    path_dict = find_file_path(path)
    action_params, cal_params = parse_json_params(action_json_file)
    # settlement = Settlement(1,
    #                         100,
    #                         1,
    #                         86400,
    #                         json.dumps(json.load(open(action_json_file))),
    #                         path_dict['verifier'])
    settlement = Settlement(cal_params, action_params, path_dict['verifier'])
    bill_generate, sync_account_generate, account_generate, account_total_generate = settlement.generate_account_flow()

    account, account_total = ParseConsoleFile(path_dict['console']).parse_console_file()
    bill = ParseBillFile(path_dict['bill']).parse_bill_file()
    sync_account = ParseSyncAccountFile(path_dict['sync_account']).parse_sync_account()

    bill_compare(bill, bill_generate)
    sync_account_compare(sync_account, sync_account_generate)
    account_total_compare(account_total, account_total_generate)
    account_compare(account, account_generate)


if __name__ == "__main__":
    main(sys.argv[1:])
