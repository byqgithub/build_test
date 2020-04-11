# -*- coding: utf-8 -*-

import os
import re

from settlement_check.utile import g_logger
from settlement_check.constant import Constant
from settlement_check.utile import id_to_name


class ParseConsoleFile(object):
    """ Parse console file, fetch all members balance and locked info
        and total change info

    Attributes:
        file_path:       console file path
        account_pattern: regex for parse account flow log
        total_pattern:   regex for parse account total change log

    Raise:
        console file can not find
    """

    def __init__(self, path):
        """ init class

        Args:
            path: console file path

        Raise:
            console file can not find
        """
        self.file_path = path
        self.account_pattern = Constant.PATTER_DICT['account']
        self.total_pattern = Constant.PATTER_DICT['total_account']
        if not os.path.exists(path):
            g_logger.exception("Path %s not found" % path)

    def parse_console_file(self):
        """ read file, search account info

        Return:
            account_total:  account total change
            account:        all members account flow;
            member--|
                    |- initial---------|-balance
                    |                  |-locked
                    |
                    |- pre_settlement--|-balance
                    |                  |-locked
                    |
                    |- post_settlement-|-balance
                                       |-locked
        """
        info_list = list()
        account = dict()
        account_total = dict()
        with open(self.file_path, encoding='utf-8', errors='ignore') as f:
            for line in f:
                r = re.search(self.account_pattern, line)
                if r is not None and len(r.groups()) >= 3:
                    info_list.append(r.groupdict())

                if Constant.TOTAL_KEYWORD in line:
                    data = line.partition(Constant.TOTAL_KEYWORD)[2].strip()
                    account_total = re.search(self.total_pattern, data).groupdict()

        for i in range(0, len(info_list), 2):
            for j in range(2):
                name = info_list[i+j].get("name")
                id_member = id_to_name(info_list[i+j].get("id"))
                value = info_list[i+j].get("value")
                if id_member not in account:
                    account[id_member] = {Constant.CHECK_POINT[0]: {name: value}}
                else:
                    n = len(account[id_member].keys())
                    if 0 < n <= len(Constant.CHECK_POINT):
                        if len(account[id_member][Constant.CHECK_POINT[n - 1]]) < 2:
                            account[id_member][Constant.CHECK_POINT[n - 1]].update({name: value})
                        else:
                            if n < len(Constant.CHECK_POINT):
                                if Constant.CHECK_POINT[n] not in account[id_member].keys():
                                    account[id_member][Constant.CHECK_POINT[n]] = dict()
                                account[id_member][Constant.CHECK_POINT[n]].update({name: value})

        return account, account_total


class ParseBillFile(object):
    """ Parse bill file, fetch trade flow and account flow

    Attributes:
        file_path:     bill file path
        bill_pattern:  account flow pattern

    Raise:
        bill file can not find
    """

    def __init__(self, path):
        """ init class

        Args:
            path: bill file path

        Raise:
            bill file can not find
        """
        self.file_path = path
        self.bill_pattern = Constant.PATTER_DICT['bill']
        if not os.path.exists(path):
            g_logger.exception("Path %s not found" % path)

    def __merge_account_flow(self, flow):
        """ Merge account flow about miner reward

        Args:
            flow: raw account flow

        Return:
            a list of merged account flow
        """
        type_name = "MinerReward"
        merge_dict = dict()
        modify_id = list()
        del_id = list()
        for i, account in enumerate(flow):
            action = account.get('action', '')
            if type_name in account.get('type', '') and action:
                if action in merge_dict.keys():
                    merge_dict[action] += float(account.get('amount', 0))
                    del_id.append(i)
                else:
                    merge_dict[action] = float(account.get('amount', 0))
                    modify_id.append(i)

        for index in modify_id:
            flow[index]['receiver'] = re.search("(?P<type>\D+)\d*", flow[index]['receiver'])['type']
            flow[index]['amount'] = str(merge_dict[flow[index]['action']])
        for num, index in enumerate(del_id):
            flow.pop(index - num)

    def parse_bill_file(self):
        """ Parse file content, fetch account flow

        Return:
            trade flow and account flow
        """
        bill_dict = {'fee': list(), 'refund': list(), 'reward': list()}
        with open(self.file_path, encoding='utf-8') as f:
            for line in f:
                regex = re.search(self.bill_pattern, line)
                if regex is not None:
                    record = regex.groupdict()
                    record['payer'] = id_to_name(member_id=record['payer'])
                    record['receiver'] = id_to_name(member_id=record['receiver'])
                    if 'fee' in record['type'].lower():
                        bill_dict['fee'].append(record)
                    if 'refund' in record['type'].lower():
                        bill_dict['refund'].append(record)
                    if 'reward' in record['type'].lower():
                        bill_dict['reward'].append(record)

        # self.__merge_account_flow(bill)
        return bill_dict


class ParseSyncAccountFile(object):
    """ Parse all members revenue and refund and expense

    Attributes:
        file_path:            sync account file path
        sync_account_pattern: account flow pattern

    Raise:
        sync account file can not find
    """

    def __init__(self, path):
        """ init class

        Args:
            path: sync account file path

        Raise:
            sync account file can not find
        """
        self.file_path = path
        self.sync_account_pattern = Constant.PATTER_DICT['sync_account']
        if not os.path.exists(path):
            g_logger.exception("Path %s not found" % path)

    def parse_sync_account(self):
        """ Parse sync account file, fetch revenue and refund and expense info

        Return:
            revenue and refund and expense info
            summary-|
                    |- revenue--|-receiver-|-amount
                    |           |......
                    |
                    |- expense--|-receiver-|-amount
                    |           |......
                    |
                    |- refund-—-|-receiver-|-amount
                    |           |......
        """
        summary = dict()
        with open(self.file_path, encoding='utf-8') as f:
            for line in f:
                record = re.search(self.sync_account_pattern, line)
                if record['type'] not in summary.keys():
                    summary[record['type']] = dict()
                summary[record['type']].update({id_to_name(record['receiver']): record['amount']})
        return summary


class ParseVerifyAmount(object):
    """ Read verifier file, cals verify amount

    Attributes:
        file_path:   verifier log path
        pattern:     verify flow pattern

    Raise:
        Verifier log can not find
    """

    def __init__(self, path):
        """ init class

        Args:
            path: verifier log path

        Raise:
            Verifier log can not find
        """
        self.file_path = path
        self.pattern = Constant.PATTER_DICT['verify']
        if not os.path.exists(path):
            g_logger.exception("Path %s not found" % path)

    def parse_verifier_file(self):
        """ Parse verifier file, fetch verify workload for reward statistic

        Return:
            all member workload about one verifier:
            workload----|
                        |- miner0---|-PoST--|-verify amount
                        |           |-PoLC--|-verify amount
                        |           |-PoRep-|-verify amount
                        |           |-PoMD--|-verify amount
                        |
                        |- user0 -—-|-PoST--|-verify amount
                        |           |-PoLC--|-verify amount
                        |           |-PoRep-|-verify amount
                        |           |-PoMD--|-verify amount
                        ......
        """
        workload = dict()
        with open(self.file_path, encoding='utf-8') as f:
            for line in f:
                record = re.search(self.pattern, line)
                if record is None:
                    continue

                record_dict = record.groupdict()
                verify_type = record_dict.get('type', '').lower()
                initiator = id_to_name(record_dict.get('initiator', ''))
                # verifier = id_to_name(record_dict.get('verifier', ''))
                # if verifier not in workload.keys():
                #     workload[verifier] = dict()
                if initiator not in workload.keys():
                    workload[initiator] = dict().fromkeys(['post', 'polc', 'porep', 'pomd'], 0)
                workload[initiator][verify_type] += 1
        return workload


if __name__ == "__main__":
    console = ParseConsoleFile(r"D:\test_log\CPool_del_pass\TestObjectActionsWithCPool.txt")
    # console = ParseConsoleFile(r"D:\test_log\CPool_del_pass\new 3.txt")
    bill = ParseBillFile(r'D:\test_log\CPool_del_pass\2018-10-17\bill.log')
    sync_account = ParseSyncAccountFile(r'D:\test_log\CPool_del_pass\2018-10-17\sync_account.log')
    verify = ParseVerifyAmount(r'D:\test_log\CPool_del_pass\2018-10-17\verifier.2018-10-17.log')
    console.parse_console_file()
    bill.parse_bill_file()
    sync_account.parse_sync_account()
    verify.parse_verifier_file()
