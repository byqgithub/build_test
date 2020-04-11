# -*- coding: utf-8 -*-


class Constant(object):
    """ constant """

    # members id
    NAME_ID = {"user0": "002508021221033fb36e1471d2153d0759e14386c6c294b1ad09244841ee8d043eadd1bfe7baaa",
               "user1": "002508021221024d8a69222ab1b305aa6abd5615058ed0e7e9f4da04e190284bbfb5fae968b348",
               "miner0": "00250802122102ee1ee28040a7ac46cf4328c648caa456caa3b74b6948246201c95a461cb27e92",
               "miner1": "00250802122103f940c8255c896971f911e62d18c95c1042c4c88eb1106dc43ad0ee1a1d163f27",
               "miner2": "0025080212210309726a5d82761713653145d338c18be15d5c3981cb9ce366ca62270155d3309e",
               "miner3": "0025080212210230a471de08f810db4e3ba373d506b9039b776f45fbad1c3e73881dce4a66af1e",
               "cpool": "00250802122103213cc8a7fb7b53308a3712cb9b13c90ffed1b2dc97d28b48162e454783ea213a",
               "indexer": "00250802122102ec8e7f2675863c26ba5f61c7b7972bd3a5c4a8276566de829390a6faf83470fc",
               "verifier": "00250802122103974c318dc943780b89f526d2c91199c1f5847687250720cee1a7ae3086c7052e"}

    ID_NAME = {"002508021221033fb36e1471d2153d0759e14386c6c294b1ad09244841ee8d043eadd1bfe7baaa": "user0",
               "002508021221024d8a69222ab1b305aa6abd5615058ed0e7e9f4da04e190284bbfb5fae968b348": "user1",
               "00250802122102ee1ee28040a7ac46cf4328c648caa456caa3b74b6948246201c95a461cb27e92": "miner0",
               "00250802122103f940c8255c896971f911e62d18c95c1042c4c88eb1106dc43ad0ee1a1d163f27": "miner1",
               "0025080212210309726a5d82761713653145d338c18be15d5c3981cb9ce366ca62270155d3309e": "miner2",
               "0025080212210230a471de08f810db4e3ba373d506b9039b776f45fbad1c3e73881dce4a66af1e": "miner3",
               "00250802122103213cc8a7fb7b53308a3712cb9b13c90ffed1b2dc97d28b48162e454783ea213a": "cpool",
               "00250802122102ec8e7f2675863c26ba5f61c7b7972bd3a5c4a8276566de829390a6faf83470fc": "indexer",
               "00250802122103974c318dc943780b89f526d2c91199c1f5847687250720cee1a7ae3086c7052e": "verifier"}

    RAW_ACCOUNT = 1000000000
    RAISE_AMOUNT = 100000

    CHECK_POINT = ("initial", "pre_settlement", "post_settlement")

    TOTAL_KEYWORD = "CalcTotalChange"

    PATTER_DICT = {"account":       "(?P<name>\w+)\s+coins of\s+(?P<id>\w+):\s*(?P<value>\d+).*", # .*\[CheckCoins\]\s*,
                   "total_account": "(?P<revenue>\d+)\s+(?P<expense>\d+)\s+(?P<remain>\d+)\s+(?P<refund>\d+)\s*",
                   "bill":          ".+,(?P<type>.*),(?P<payer>.*),(?P<receiver>.*),(?P<amount>.*),(?P<action>.*),.*,(?P<owner>.*).*",
                   "sync_account":  ".+,(?P<type>\w+),(?P<receiver>\w+),(?P<amount>\d+).*",
                   "verify":        ".+,(?P<type>.+),(?P<initiator>.+),(?P<verifier>.+),.+,.+,.+,.+,.+"}

    FILE_DICT = {'bill':         '^bill.log$',
                 'sync_account': 'sync_account.log',
                 'verifier':     'verifier.\d+-\d+-\d+.log',
                 'console':      'console.log'}

    LOG_PATH = './settlement.log'
