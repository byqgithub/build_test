# -*- coding: utf-8 -*-

from math import ceil, floor
from settlement_check.constant import Constant


def put_object_funds(gas_price, seg_count, seg_copy_num, duration, is_laxity=False):
    """ put object funds

    Args:
        gas_price:
        seg_count:
        seg_copy_num:
        duration:
        is_laxity:

    Return:
        funds
    """
    gas_per_seg_unit = 1 * 24
    seg_unit_count = seg_count * seg_copy_num * (16 * 1024 / 256)
    settlement_period = ceil(duration / (60 * 60 * 24))
    laxity = 1.2 if is_laxity is True else 1.0
    funds = floor(gas_price * seg_unit_count * gas_per_seg_unit * settlement_period * laxity)
    return int(funds)


def get_object_funds(gas_price, seg_count, is_laxity=False):
    """ get object funds

    Args:
        gas_price:
        seg_count:
        is_laxity:

    Return:
        funds
    """
    gas_per_seg_unit = 10
    seg_unit_count = seg_count * (16 * 1024 / 256)
    laxity = 1.2 if is_laxity is True else 1.0
    funds = floor(gas_price * seg_unit_count * gas_per_seg_unit * laxity)
    return int(funds)


def indexer_fee():
    """ Indexer fee """
    return 20000


def verifier_fee():
    """ verification fee """
    return 30


def miner_reward_polc():
    return Constant.RAISE_AMOUNT * 0.9 * 0.1


def miner_reward_post():
    return Constant.RAISE_AMOUNT * 0.9 * 0.4


def miner_reward_pomd():
    return Constant.RAISE_AMOUNT * 0.9 * 0.3


def miner_reward_rep():
    return Constant.RAISE_AMOUNT * 0.9 * 0.2


def indexer_reward():
    return Constant.RAISE_AMOUNT * 0.01


def verifier_reward():
    return Constant.RAISE_AMOUNT * 0.04


def tmp():
    return 0


PutObject = RenewObject = CopyObject = put_object_funds
GetObject = get_object_funds
RequestScheduleTask = indexer_fee
UpdateObjectAcl = DeleteObject = tmp


# print(put_object_funds(100, 1, 1, 864000, is_laxity=True))
