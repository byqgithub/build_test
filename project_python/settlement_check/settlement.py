# -*- coding: utf-8 -*-

import re
import json
from copy import deepcopy

from settlement_check import common
from settlement_check.utile import g_logger
from settlement_check.constant import Constant
from settlement_check.account_analysis import ParseVerifyAmount


class Settlement(object):
    """ All account settlement: parse action flow, generate bill, sync_account, total change and account change

    import params: action flow
    action flow json format:
        "action":
            {"member": "user0",            # action executor
             "cpool": true,                # if cpool settlement
             "action": "PutObject",        # member action
             "fee": {                      # fee flow
                 "indexer": "PutObject",
                 "miner0": "PoST",
                 "verifier": "PoST",
             },
             "refund": {                      # refund flow
                 "user0": "StorageContract",
                 "miner0": "StorageContract"
             },
             "reward": {                      #reward flow
                "miner0": ["PoLC", "PoST"],
                "other": ["indexer", "verifier"]
             }
            }

    Attributes:
        gas_price:
        seg_count:
        seg_copy_num:
        duration:
        action_flow:
        verifier_log_path: verifier log path
    """

    def __init__(self, cal_params, action_flow, verifier_log_path):
        """ init """
        self.gas_price = cal_params['gas_price']
        self.seg_count = cal_params['seg_count']
        self.seg_copy_num = cal_params['seg_copy_num']
        self.duration = cal_params['duration']
        self.action_flow = action_flow
        self.verifier_file = verifier_log_path

    def __get_attr(self, module, attr):
        """ get attribute about account settlement

        Args:
            module: module name
            attr:   attribute name

        Raise:
            Can not get attribute
        """
        try:
            obj = getattr(common, attr)
            return obj
        except AttributeError:
            g_logger.exception("Can not get attribute %s from module %s" % (attr, module))

    def __init_account_flow(self, account_dict, member):
        """ Init account flow data

        Args:
            account_dict: account dict
            member:       member list
        """
        for m in member:
            tmp_dict = dict()
            tmp_dict['initial'] = {'balance': Constant.RAW_ACCOUNT, "locked": 0}
            tmp_dict['pre_settlement'] = {'balance': Constant.RAW_ACCOUNT, "locked": 0}
            tmp_dict['post_settlement'] = {'balance': Constant.RAW_ACCOUNT, "locked": 0}
            account_dict[m] = tmp_dict

    def generate_fee_record(self, member, is_cpool, behavior, flow_dict, fee_record, member_list):
        """ Generate bill record base on action params

        Args:
            member:      action executor
            is_cpool:    if cpool settlement
            behavior:    member action
            flow_dict:   trade flow for the member
            fee_record:  fee record for the member
            member_list: member list

        Return:
            fee flow record
        """
        for item in flow_dict:
            type_name = re.search("(?P<type>\D+)\d*", item)['type']
            fee_dict = {'type': type_name.title() + "Fee"}
            if 'user' in member:
                fee_dict.update({"payer": 'cpool' if is_cpool else member})
            else:
                fee_dict.update({"payer": member})
            fee_dict.update({"receiver": item})
            if item not in member_list:
                member_list.append(item)
            if 'miner' in type_name:
                func = self.__get_attr('common', behavior)
                cost = func(self.gas_price, self.seg_count, self.seg_copy_num, self.duration)
            else:
                cost = self.__get_attr('common', type_name + '_fee')()
            fee_dict.update({"amount": cost})
            fee_dict.update({"action": flow_dict[item]})
            fee_dict.update({"owner": member if 'cpool' in fee_dict['payer'] else 'nil'})
            g_logger.debug("Bill content: %s" % fee_dict)
            fee_record.append(fee_dict)

    def generate_refund_record(self, member, is_cpool, behavior, flow_dict, refund_record):
        """ Generate refund record base on action params

        Args:
            member:        action executor
            is_cpool:      if cpool settlement
            behavior:      member action
            flow_dict:     trade flow for the member
            refund_record: refund record for the member

        Return:
            refund flow record
        """
        for item in flow_dict:
            type_name = re.search("(?P<type>\D+)\d*", item)['type']
            refund_dict = {'type': type_name.title() + "Refund"}
            if 'user' in type_name:
                refund_dict.update({"payer": 'cpool' if is_cpool else item})
                refund_dict.update({"receiver": 'cpool' if is_cpool else item})
            else:
                refund_dict.update({"payer": item})
                refund_dict.update({"receiver": item})
            func = self.__get_attr('common', behavior)
            cost = func(self.gas_price, self.seg_count, self.seg_copy_num, self.duration, is_laxity=True)
            verifier_fee = int(flow_dict[item]) * self.__get_attr('common', 'verifier_fee')()
            if 'user' in type_name:
                cost = cost - func(self.gas_price, self.seg_count, self.seg_copy_num, self.duration) - verifier_fee
            refund_dict.update({"amount": cost})
            refund_dict.update({"action": 'StorageContract'})
            refund_dict.update({"owner": member if 'cpool' in refund_dict['payer'] else 'nil'})
            g_logger.debug("Refund content: %s" % refund_dict)
            refund_record.append(refund_dict)

    def __workload_ratio(self, member, verify_type):
        """ miner Workload ratio """
        workload = ParseVerifyAmount(self.verifier_file).parse_verifier_file()
        member_workload = workload.get(member, dict()).get(verify_type, 0)
        total_workload = 0
        member_type = re.search("(?P<type>\D+)\d*", member)['type']
        for key in workload:
            if member_type in key:
                total_workload += workload.get(key, dict()).get(verify_type, 0)
        if total_workload:
            return member_workload / total_workload
        else:
            return 1

    def generate_reward_record(self, flow_dict, reward_record):
        """ Generate reward record base on action params

        Args:
            flow_dict:     trade flow for the member
            reward_record: reward record for the member

        Return:
            reward flow record
        """
        for item in flow_dict:
            reward_dict = dict()
            if 'miner' in item:
                for category in flow_dict[item]:
                    reward_dict.update({"type": "MinerReward"})
                    reward_dict.update({"payer": ""})
                    reward_dict.update({"receiver": item})
                    ratio = self.__workload_ratio(item, str(category).lower())
                    func = self.__get_attr('common', "miner_reward_" + str(category).lower())
                    reward_dict.update({"amount": int(func() * ratio)})
                    reward_dict.update({"action": category})
                    reward_dict.update({"owner": 'nil'})
                    g_logger.debug("Reward content: %s" % reward_dict)
                    reward_record.append(deepcopy(reward_dict))
            else:
                for member in flow_dict[item]:
                    type_name = re.search("(?P<type>\D+)\d*", member)['type']
                    reward_dict.update({'type': type_name.title() + "Reward"})
                    reward_dict.update({"payer": ''})
                    reward_dict.update({"receiver": member})
                    cost = self.__get_attr('common', type_name + '_reward')()
                    reward_dict.update({"amount": int(cost)})
                    reward_dict.update({"action": ''})
                    reward_dict.update({"owner": 'nil'})
                    g_logger.debug("Reward content: %s" % reward_dict)
                    reward_record.append(deepcopy(reward_dict))

    def generate_sync_account(self, bill_dict, sync_account_dict):
        """ Generate sync account

        Args:
            bill_dict:           bill info dict
            sync_account_dict:   sync account info dict
        """
        for item in bill_dict['fee']:
            sync_account_dict['expense'][item['payer']] = item['amount'] + \
                                                          sync_account_dict['expense'].get(item['payer'], 0)
            sync_account_dict['revenue'][item['receiver']] = item['amount'] + \
                                                             sync_account_dict['revenue'].get(item['receiver'], 0)

        for item in bill_dict['reward']:
            sync_account_dict['revenue'][item['receiver']] = item['amount'] + \
                                                             sync_account_dict['revenue'].get(item['receiver'], 0)

        for item in bill_dict['refund']:
            sync_account_dict['refund'][item['payer']] = item['amount'] + \
                                                         sync_account_dict['refund'].get(item['payer'], 0)
        for category in sync_account_dict:
            for obj in sync_account_dict[category]:
                g_logger.debug("Category:%s; Entity:%s; amount:%s" % (category, obj, sync_account_dict[category][obj]))

    def generate_account_total(self, sync_account_dict, total_change_dict):
        """ Generate total change

        Args:
            sync_account_dict:   bill info dict
            total_change_dict:   total change info dict
        """
        for item in sync_account_dict['revenue']:
            total_change_dict['revenue'] += sync_account_dict['revenue'][item]

        for item in sync_account_dict['expense']:
            total_change_dict['expense'] += sync_account_dict['expense'][item]

        for item in sync_account_dict['refund']:
            total_change_dict['refund'] += sync_account_dict['refund'][item]
            total_change_dict['remain'] = total_change_dict['revenue'] - total_change_dict['expense']

        g_logger.debug("revenue: %s; expense: %s; remain: %s; refund: %s" % (total_change_dict['revenue'],
                                                                             total_change_dict['expense'],
                                                                             total_change_dict['remain'],
                                                                             total_change_dict['refund']))

    def generate_account_change(self, bill_dict, account_change_dict, members):
        """ Generate all account change

        Args:
            bill_dict:           bill info dict
            account_change_dict: account change info dict
            members:             member info list
        """
        self.__init_account_flow(account_change_dict, members)
        has_locked = list()
        for record in bill_dict['fee']:
            amount = record['amount']
            if 'verifier' in record['receiver']:
                continue
            if 'miner' in record['receiver'] and record['receiver'] not in has_locked:
                account_change_dict[record['receiver']]['pre_settlement']['balance'] -= amount * 1.2
                account_change_dict[record['receiver']]['pre_settlement']['locked'] += amount * 1.2
                account_change_dict[record['receiver']]['post_settlement']['balance'] -= amount * 1.2
                account_change_dict[record['receiver']]['post_settlement']['locked'] += amount * 1.2
                has_locked.append(record['receiver'])
            if 'miner' in record['receiver']:
                amount = amount * 1.2
            account_change_dict[record['payer']]['pre_settlement']['balance'] -= amount
            account_change_dict[record['payer']]['pre_settlement']['locked'] += amount
            account_change_dict[record['payer']]['post_settlement']['balance'] -= amount
            account_change_dict[record['payer']]['post_settlement']['locked'] += amount

        for record in bill_dict['fee']:
            account_change_dict[record['payer']]['post_settlement']['locked'] -= record['amount']
            account_change_dict[record['receiver']]['post_settlement']['balance'] += record['amount']
        for record in bill_dict['refund']:
            amount = record['amount']
            account_change_dict[record['payer']]['post_settlement']['locked'] -= amount
            account_change_dict[record['receiver']]['post_settlement']['balance'] += amount
        for record in bill_dict['reward']:
            account_change_dict[record['receiver']]['post_settlement']['balance'] += record['amount']

        for key in account_change_dict:
            g_logger.debug("member: %s; detail: %s" % (key, account_change_dict[key]))

    def generate_account_flow(self):
        """ Generate account flow base on action flow """
        member_list = list()
        bill = {'fee': list(), 'refund': list(), 'reward': list()}
        sync_account = {'revenue': dict(), 'expense': dict(), 'refund': dict()}
        account_flow = dict()
        total_change = {'revenue': 0, 'expense': 0, 'remain': 0, 'refund': 0}
        for item in self.action_flow:
            action = self.action_flow[item]
            member = action.get('member', '')
            if member not in member_list:
                member_list.append(member)

            is_cpool = action.get('cpool', False)
            if is_cpool and 'cpool' not in member_list:
                member_list.append('cpool')

            behavior = action.get('action', '')
            g_logger.debug("Member: %s; is cpool: %s; behavior: %s" % (member, is_cpool, behavior))
            if 'fee' in action.keys():
                self.generate_fee_record(member, is_cpool, behavior, action['fee'], bill['fee'], member_list)
            if 'refund' in action.keys():
                self.generate_refund_record(member, is_cpool, behavior, action['refund'], bill['refund'])
            if 'reward' in action.keys():
                self.generate_reward_record(action['reward'], bill['reward'])

        self.generate_sync_account(bill, sync_account)
        self.generate_account_total(sync_account, total_change)
        self.generate_account_change(bill, account_flow, member_list)

        return bill, sync_account, account_flow, total_change


if __name__ == "__main__":
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

    # s = Settlement(1,
    #                100,
    #                1,
    #                86400,
    #                json.dumps(action_flow),
    #                r'D:\test_log\CPool_del_pass\2018-10-17\verifier.2018-10-17.log')
    # s.generate_account_flow()
