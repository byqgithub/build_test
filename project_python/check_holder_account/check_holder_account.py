# -*- coding: utf-8 -*-

import os
import sys
import csv
import json
import time
import getopt
import logging
import pymysql
import datetime
import requests

usage = """
USAGE:
   --config_file:    config file path
   --result_output:  result output dir
   check_holder_account.py --config_file=<config_file_path> --result_output=<result_output_dir>

example:
   check_holder_account.py --config_file=/home/config.json --result_output=/home/result
"""

sql_command_dict = {"query_account": "select id, balance, locked_balance from account;"}


class RpcWorker(object):
    """  """

    def __init__(self, config, logger):
        self.headers = config["headers"]
        self.timeout = config["timeout"]
        self.internal = config["internal"]
        self.tag = "rpc: || "
        self.logger = logger

    def worker(self, url, headers, data):
        ret = None
        time.sleep(1)
        for i in range(5):
            try:
                response = requests.post(url, data=data, headers=headers, timeout=self.timeout)
                self.logger.info("rpc response: %s" % response)
                if response.status_code == 200:
                    ret = response.text
                    self.logger.info("rpc response txt: %s" % ret)
                    break
                time.sleep(self.internal)
            except Exception as err:
                self.logger.error(self.tag + str(err))
        return ret

    def handle(self, ip, port, command, params, host_type="chain"):
        if "chain" in host_type:
            url = "http://{}:{}/v1/user/accountstate".format(ip, port)
            body = {"address": params}
        else:
            url = "http://{}:{}/rpc".format(ip, port)
            body = {"jsonrpc": "2.0", "method": command, "params": params, "id": 1}
        data = json.dumps(body)
        self.logger.info("rpc url: %s" % url)
        self.logger.info("rpc data: %s" % data)
        return self.worker(url, self.headers, data)


class MysqlDB(object):
    """  """

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def handle(self, command):
        """ """
        try:
            db = pymysql.connect(self.config.get("host"),
                                 self.config.get("user"),
                                 self.config.get("password"),
                                 self.config.get("db"))
            try:
                cursor = db.cursor()
                if ";" not in command:
                    command = command + ";"
                self.logger.info("Sql cmd: %s" % command)
                cursor.execute("START TRANSACTION WITH CONSISTENT SNAPSHOT;")
                cursor.execute(command)
                db.commit()
                ret = cursor.fetchall()
            except Exception as err:
                ret = None
                self.logger.error(err)
                db.rollback()
            finally:
                db.close()
        except Exception as err:
            ret = None
            self.logger.error("Can't connect to MySQL server: %s" % err)

        return ret


class CheckAccount(object):
    """  """
    def __init__(self, config, logger, output_path):
        self.db_config = config.get("mysql", dict())
        self.rpc_config = config.get("rpc", dict())
        self.chain_config_list = config.get("ppio_chain", list())
        self.logger = logger
        self.output_path = output_path
        self.db = MysqlDB(self.db_config, self.logger)
        self.rpc = RpcWorker(self.rpc_config, self.logger)

    def query_holder_balance(self):
        """  """
        holder_balance = 0
        for chain_config in self.chain_config_list:
            ip = chain_config.get("ip", None)
            port = chain_config.get("port", None)
            addr = chain_config.get("addr", None)
            if ip is not None and port is not None and addr is not None:
                ret = self.rpc.handle(ip, port, "", addr)
                if ret is None:
                    self.logger.error("Rpc response is None")
                    continue

                ret = ret.replace("\n", "")
                ret = ret.replace("\\n", "")
                self.logger.debug("Rpc response ret %s" % ret)
                ret = json.loads(ret)
                self.logger.debug("Rpc response ret json %s" % ret)
                if ("result" in ret.keys()
                        and isinstance(ret.get("result"), dict)
                        and "balance" in ret.get("result").keys()):
                    tmp_str = ret.get("result").get("balance")
                    try:
                        holder_balance = int(tmp_str)
                        break
                    except ValueError as err:
                        self.logger.error("Parse holder account info err: %s" % err)
            else:
                self.logger.info("Fetch node ip and port error")
        else:
            self.logger.error("Query holder account balance error")

        self.logger.info("Holder balance: %s" % holder_balance)
        print("Holder balance: %s" % holder_balance)
        return holder_balance

    def fetch_account_info(self):
        """  """
        cmd = sql_command_dict.get("query_account")
        ret = self.db.handle(cmd)
        total_coin = 0
        if isinstance(ret, tuple):
            for info in ret:
                if len(info) >= 3:
                    try:
                        total_coin += int(info[1])
                        total_coin += int(info[2])
                    except ValueError as err:
                        self.logger.error("Convert account info err: %s" % err)

        self.logger.info("All account total coin: %s" % total_coin)
        print("All account total coin: %s" % total_coin)
        return total_coin

    def check_holder_account(self):
        """  """
        result = False
        headers = list()
        holder_balance = self.query_holder_balance()
        total_coin = self.fetch_account_info()
        if holder_balance == total_coin:
            result = True

        current_time = datetime.datetime.now()
        timestamp = datetime.datetime.strftime(current_time, "%Y-%m-%d_%H-%M-%S")
        rows = [(timestamp+"\t", str(result)+"\t", str(holder_balance)+"\t", str(total_coin))]

        csv_file = os.path.join(self.output_path, "check_result.csv")
        if not os.path.exists(csv_file):
            headers = ['Time\t', 'result\t', 'holder\t', 'account']
        with open(csv_file, 'a') as f:
            f_csv = csv.writer(f)
            if headers:
                f_csv.writerow(headers)
            f_csv.writerows(rows)

        return result


def set_logger(timestamp, path="", category="log", clear_handler=False):
    """ Set logger system """
    logger_name = 'check_holder_account'
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    if clear_handler:
        for handler in logger.handlers:
            logger.removeHandler(handler)

    dir_name = "log" if "log" in category else "result"
    if path:
        log_path = os.path.join(path, dir_name, "%s_%s.log" % (dir_name, timestamp))
    else:
        log_path = os.path.join(os.getcwd(), dir_name, "%s_%s.log" % (dir_name, timestamp))

    if not os.path.exists(os.path.dirname(log_path)):
        os.makedirs(os.path.dirname(log_path))
        print('Create log dir: %s' % os.path.dirname(log_path))

    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    log_format = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
    data_format = "%a %d %b %Y %H:%M:%S"
    formatter = logging.Formatter(log_format, data_format)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def parse_argv(argv):
    """  """
    config_file = ""
    output_path = os.getcwd()

    try:
        opts, args = getopt.getopt(argv, "hc:r:", ["config_file=", "result_output=", "help"])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print(usage)
            sys.exit(2)
        elif opt in ("-c", "--config_file"):
            config_file = os.path.abspath(arg)
            if not os.path.exists(config_file):
                print('action config file do not exit')
                sys.exit(2)
            else:
                print("config path: %s" % config_file)
        elif opt in ("-r", "--result_output"):
            output_path = os.path.abspath(arg)

            if not os.path.exists(output_path):
                os.makedirs(output_path)

            if not os.path.exists(output_path):
                print('result output dir do not exit')
                sys.exit(2)
            else:
                print("result output path: %s" % output_path)

    return config_file, output_path


def main(argv):
    """ main """
    config_file, output_path = parse_argv(argv)

    current_time = datetime.datetime.now()
    timestamp = datetime.datetime.strftime(current_time, "%Y-%m-%d_%H-%M-%S")
    g_logger = set_logger(timestamp, output_path, clear_handler=True)

    try:
        config = json.load(open(config_file))
    except:
        g_logger.error("Can not convert config")
        sys.exit(1)

    g_logger.info("config file: %s" % config_file)
    g_logger.info("config content: %s" % config)
    g_logger.info("outfile path: %s" % output_path)
    checker = CheckAccount(config, g_logger, output_path)
    check_result = checker.check_holder_account()
    if check_result:
        print("Check time: %s, holder account check successful" % timestamp)
        sys.exit(0)
    else:
        print("Check time: %s, holder account check failed" % timestamp)
        sys.exit(1)


if "__main__" == __name__:
    main(sys.argv[1:])
