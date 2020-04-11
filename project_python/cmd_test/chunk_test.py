# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import shlex
import getopt
import shutil
import logging
import datetime
import subprocess

commend_dict = {"start_user": r"screen -dmS \"ppiox.user%s\" -L -Logfile %s/user%s.log %s/ppio daemon start --datadir=%s",
                "start_miner": r"screen -dmS \"ppiox.miner%s\" -L -Logfile %s/miner%s.log %s/miner daemon start --datadir=%s",

                "import_chunk": r"%s/ppio --rpcport=%s chunk import  %s",
                "put_chunk": r"%s/ppio chunk put --copies=%s --duration=%s --chiprice=%s --rpcport=%s %s",
                "get_chunk": r"%s/ppio chunk get --chiprice=%s --rpcport=%s %s",
                "get_chunk_status": r"%s/ppio chunk status --rpcport=%s %s",
                "get_miner_chunk_status": r"%s/miner chunk list --rpcport=%s",
                "delete_chunk": r"%s/ppio chunk delete --rpcport=%s %s",

                "": "",
                }

user_key = {18060: "7de2a8082da8e0b13ad778d9850282a8e0775546c0d23132653d301c4881b184",
            18061: "9165f52b9f3c141d42fbb527a0045cef0774483eae19570ef35143272f1a88d1",
            18062: "4c8aa6c363d14cb597dbdb9b5bdc7e08905ce6e8993a3e56471ae3c79e30a6eb"}

user_rpc_port = 18060
miner_rpc_port = 18050
#g_logger = ""


def set_logger(path=""):
    """ Set logger system """
    logger_name = 'chunk_test'
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    for handler in logger.handlers:
        logger.removeHandler(handler)

    if path:
        log_path = os.path.join(path, "chunk_test.log")
    else:
        log_path = os.path.join(os.getcwd(), "chunk_test.log")
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    log_format = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
    data_format = "%a %d %b %Y %H:%M:%S"
    formatter = logging.Formatter(log_format, data_format)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def exec_shell(command, shell=False, timeout=200):
    """ Exec shell cmd

    Args:
        command:
        shell:
        timeout:

    Return:
    Except:
    """
    try:
        g_logger.debug("cmd: %s" % command)
    except NameError:
        print("cmd: %s" % command)
    if not shell:
        command = shlex.split(command)
    try:
        result = subprocess.check_output(command, shell, timeout=timeout, stderr=subprocess.STDOUT).decode('utf-8')
        # g_logger.debug("result: %s" % result)
        return result
    except subprocess.CalledProcessError as e:
        try:
            g_logger.error("[ERROR] Execute shell command err: %s" % e)
        except NameError:
            print("[ERROR] Execute shell command err: %s" % e)


def string_filter(flag, result_string):
    """  """
    flag = "\n"
    if result_string.lower():
        try:
            output = result_string.partition(flag)[2].strip()
            g_logger.debug("filter output result: %s" % output)
        except IndexError:
            output = ""
            g_logger.error("[ERROR] Command output parse error")
        return output


def start_server(start_time):
    """ start gppio and ppio server node """
    cmd = r"%s %s %s %s" % (os.path.abspath(os.path.join(os.getcwd(), "start_server.sh")),
                            "/home/workspace/go",
                            os.path.abspath(os.getcwd()),
                            start_time)
    os.system(cmd)


def stop_server(miner_clean=False):
    """ stop gppio and ppio server node """
    clean = "miner_clean" if miner_clean else ""
    cmd = r"%s %s %s" % (os.path.abspath(os.path.join(os.getcwd(), "stop_server.sh")), "/home/workspace/go", clean)
    os.system(cmd)


# def stop_user_miner():
#     """ stop user and miner node """
#     cmd = "sh " + os.path.abspath(os.path.join(os.getcwd(), "stop_users_miners.sh"))
#     exec_shell(cmd)


def start_user(bin_path, amount=1, start_time=""):
    """ Start user

    Args:
        bin_path:
        amount:     user amount
        start_time: start user time
    """
    user_list = list()
    log_folder_name = os.path.join(os.path.abspath(os.getcwd()), "test_log", start_time)
    os.makedirs(log_folder_name, exist_ok=True)
    for i in range(amount):
        config_path = os.path.abspath(os.path.join(os.getcwd(), "config", "user%s" % i))
        storage_path = os.path.join(config_path, "storage")
        if os.path.exists(config_path):
            shutil.rmtree(storage_path) if os.path.exists(storage_path) else str()
            start_user_cmd = commend_dict.get("start_user", "%s %s %s %s %s") % (i, log_folder_name, i, bin_path, config_path)
            exec_shell(start_user_cmd)
            user_list.append(user_rpc_port + i)
    return user_list


def start_miner(bin_path, amount=1, start_time=""):
    """ Start miner

    Args:
        bin_path:
        amount:     miner amount
        start_time: start miner time
    """
    miner_list = list()
    log_folder_name = os.path.join(os.path.abspath(os.getcwd()), "test_log", start_time)
    os.makedirs(log_folder_name, exist_ok=True)
    for i in range(amount):
        config_path = os.path.abspath(os.path.join(os.getcwd(), "config", "miner%s" % i))
        # storage_path = os.path.join(config_path, "storage")
        if os.path.exists(config_path):
            # shutil.rmtree(storage_path) if os.path.exists(storage_path) else str()
            start_miner_cmd = commend_dict.get("start_miner", "%s %s %s %s %s") % (i, log_folder_name, i, bin_path, config_path)
            exec_shell(start_miner_cmd)
            miner_list.append(miner_rpc_port + i)
    return miner_list


def import_chunk(bin_path, file_path, rpc_port=18060):
    """  """
    g_logger.debug("File path: %s" % file_path)
    with open(file_path, 'a') as f:
        f.write("new line")
        f.flush()

    commend = commend_dict.get("import_chunk") % (bin_path, rpc_port, file_path)
    result = exec_shell(commend)
    if result.lower():
        g_logger.info("import chunk successful")
        result_json = string_filter(file_path, result)
        filter_success = True if result_json else False
        return filter_success, result_json
    else:
        g_logger.error("[ERROR] import chunk failed, error: %s" % result)
        return False, result


def put_chunk(bin_path, chunks_hash_list, copies, chi_price, duration=86400, rpc_port=18060):
    """ """
    put_chunks_status = True
    for chunk_hash in chunks_hash_list:
        time.sleep(5)
        commend = commend_dict.get("put_chunk") % (bin_path, copies, duration, chi_price, rpc_port, chunk_hash)
        result = exec_shell(commend)
        if result.lower():
            g_logger.info("put chunk successful")
        else:
            put_chunks_status = False
            g_logger.error("[ERROR] put chunk failed, error: %s" % result)
    return put_chunks_status


def get_chunk(bin_path, chunks_hash_list, chi_price, rpc_port=18060):
    """"""
    get_chunks_status = True
    for chunk_hash in chunks_hash_list:
        commend = commend_dict.get("get_chunk") % (bin_path, chi_price, rpc_port, chunk_hash)
        result = exec_shell(commend)
        # time.sleep(5)
        if result.lower():
            g_logger.info("get chunk successful")
        else:
            get_chunks_status = False
            g_logger.error("[ERROR] get chunk failed, error code: %s" % result)
    return get_chunks_status


def get_chunk_status(bin_path, chunk_hash, rpc_port=18060):
    """  """
    commend = commend_dict.get("get_chunk_status") % (bin_path, rpc_port, chunk_hash)
    result = exec_shell(commend)
    if result.lower():
        g_logger.info("get chunk status successful")
        result_json = string_filter("status", result)
        if result_json:
            result_dict = json.loads(result_json)
            g_logger.info("chunk status: %s" % result_dict)
            return True, result_dict
        else:
            return False, dict()
    else:
        g_logger.error("[ERROR] get chunk status failed, error: %s" % result)
        return False, dict()


def delete_chunk(bin_path, chunks_hash_list, rpc_port=18060):
    delete_chunks_status = True
    for chunk_hash in chunks_hash_list:
        commend = commend_dict.get("delete_chunk") % (bin_path, rpc_port, chunk_hash)
        result = exec_shell(commend)
        if "succeed" in result.lower():
            g_logger.info("delete chunk successful")
        else:
            delete_chunks_status = False
            g_logger.error("[ERROR] delete chunk failed, error code: %s" % result)
    return delete_chunks_status


def get_object_chunks_relation(bin_path, file_path, rpc_port=18060):
    """  """
    result, import_json = import_chunk(bin_path, file_path, rpc_port)
    if result:
        import_dict = json.loads(import_json)
        object_hash = import_dict.get('Hash', '')
        chunks_list = import_dict.get('Chunks', '')
        chunks_hash_list = list()
        for chunk_info in chunks_list:
            chunks_hash_list.append(chunk_info.get('Hash', ''))
        return dict({"object_hash": object_hash, "chunks_hash": chunks_hash_list})
    else:
        return dict()


def check_chunks_status_from_user(bin_path, chunks_hash_list, rpc_port=18060):
    """  """
    all_chunks_status = True
    chunks_status_list = list()
    for chunk_hash in chunks_hash_list:
        result, status_list = get_chunk_status(bin_path, chunk_hash, rpc_port)
        if not result:
            all_chunks_status = False
            chunks_hash_list.append(dict({"chunk_hash": chunk_hash, "chunk_status": 0}))
            break

        if len(status_list) > 1:
            g_logger.error("[ERROR] Chunk status format changed")
            all_chunks_status = False
            chunks_hash_list.append(dict({"chunk_hash": chunk_hash, "chunk_status": 0}))
            break

        chunk_status = 1
        for status in status_list:
            if chunk_hash in status.get("Hash", ""):
                if not status.get("Contracts"):
                    all_chunks_status = False
                    continue

                for contract in status.get("Contracts", list()):
                    chunk_status = str(contract.get("Status", 0))
                    if str(contract.get("Status", 0)) != "SC_AVAILABLE":
                        all_chunks_status = False
                        break
                chunks_status_list.append(dict({"chunk_hash": chunk_hash, "chunk_status": chunk_status}))
    g_logger.info("all chunks status: %s" % chunks_status_list)
    return all_chunks_status


def check_chunks_status_from_miner(bin_path, chunks_hash_list, rpc_port=18050):
    """  """
    all_chunks_status = True
    for chunk_hash in chunks_hash_list:
        commend = commend_dict.get("get_miner_chunk_status") % (bin_path, rpc_port)
        result = exec_shell(commend)
        if "fail" in result.lower():
            all_chunks_status = False
            g_logger.error("[ERROR] check miner chunk status failed, error: %s" % result)
        else:
            if chunk_hash not in result:
                all_chunks_status = False
                g_logger.error("[ERROR] check miner chunk status failed, error: %s" % result)
            g_logger.info("check miner chunk status successful")
    return all_chunks_status


def put_chunks_base_on_param(bin_path, file_path, user_amount, miner_amount, copies, chi_price, duration, name=""):
    """ user put object to one miner """
    check_result = False
    global g_logger
    current_time = datetime.datetime.now()
    timestamp = name + '_' + datetime.datetime.strftime(current_time, "%Y-%m-%d_%H-%M-%S")
    script_log_path = os.path.join(os.getcwd(), "test_log", timestamp)
    if not os.path.exists(script_log_path):
        os.makedirs(script_log_path, exist_ok=True)
    g_logger = set_logger(script_log_path)

    start_server(timestamp)
    miner_list = start_miner(bin_path, miner_amount, timestamp)
    user_list = start_user(bin_path, user_amount, timestamp)
    time.sleep(10)
    object_chunks = get_object_chunks_relation(bin_path, file_path, user_list[0])
    chunks_hash_list = object_chunks.get("chunks_hash", list())
    time.sleep(30)
    print("put_chunks_base_on_param %s" % chunks_hash_list)
    if chunks_hash_list:
        check_result = put_chunk(bin_path, chunks_hash_list, copies, chi_price, duration, user_list[0])
        if check_result:
            time.sleep(10)
            for miner in miner_list:
                check_result &= check_chunks_status_from_miner(bin_path, chunks_hash_list, miner)
            check_result &= check_chunks_status_from_user(bin_path, chunks_hash_list, user_list[0])
            if check_result:
                time.sleep(5)
                check_result = delete_chunk(bin_path, chunks_hash_list, user_list[0])
                if check_result:
                    time.sleep(5)
                    for miner in miner_list:
                        check_result &= check_chunks_status_from_miner(bin_path, chunks_hash_list, miner)
                    check_result = not check_chunks_status_from_user(bin_path, chunks_hash_list, user_list[0])
    else:
        check_result = False

    # stop_server()
    return check_result


def get_chunks_base_on_param(bin_path, file_path, user_amount, miner_amount, copies, chi_price, duration, ownership="self", name=""):
    """ user get object from one miner """
    check_result = False
    global g_logger
    current_time = datetime.datetime.now()
    timestamp = name + '_' + datetime.datetime.strftime(current_time, "%Y-%m-%d_%H-%M-%S")
    script_log_path = os.path.join(os.getcwd(), "test_log", timestamp)
    if not os.path.exists(script_log_path):
        os.makedirs(script_log_path, exist_ok=True)
    g_logger = set_logger(script_log_path)

    # start_server(timestamp)
    # miner_list = start_miner(bin_path, miner_amount, timestamp)
    # user_list = start_user(bin_path, user_amount, timestamp)
    # time.sleep(10)
    miner_list = [18050, 18051]
    user_list = [18060, 18061]
    object_chunks = get_object_chunks_relation(bin_path, file_path, user_list[0])
    chunks_hash_list = object_chunks.get("chunks_hash", list())
    time.sleep(30)
    print("get_chunks_base_on_param: %s" % chunks_hash_list)
    if chunks_hash_list:
        check_result = put_chunk(bin_path, chunks_hash_list, copies, chi_price, duration, user_list[0])
        time.sleep(120)
        if check_result:
            for miner in miner_list:
                check_result &= check_chunks_status_from_miner(bin_path, chunks_hash_list, miner)
            check_result &= check_chunks_status_from_user(bin_path, chunks_hash_list, user_list[0])
            if check_result:
                if "self" in ownership:
                    check_result &= get_chunk(bin_path, chunks_hash_list, chi_price, user_list[0])
                else:
                    check_result &= get_chunk(bin_path, chunks_hash_list, chi_price, user_list[1])
                if check_result:
                    for miner in miner_list:
                        check_result &= check_chunks_status_from_miner(bin_path, chunks_hash_list, miner)
                    check_result &= check_chunks_status_from_user(bin_path, chunks_hash_list, user_list[0])
                    if "self" not in ownership:
                        check_result &= check_chunks_status_from_user(bin_path, chunks_hash_list, user_list[1])
                if check_result:
                    check_result = delete_chunk(bin_path, chunks_hash_list, user_list[0])
                    if check_result:
                        time.sleep(5)
                        for miner in miner_list:
                            check_result &= check_chunks_status_from_miner(bin_path, chunks_hash_list, miner)
                        check_result &= not check_chunks_status_from_user(bin_path, chunks_hash_list, user_list[0])
                        if "self" not in ownership:
                            check_result &= check_chunks_status_from_user(bin_path, chunks_hash_list, user_list[1])
    else:
        check_result = False

    # stop_server()
    return check_result


def put_small_object_one_copy(bin_path, file_path):
    """ one user put 128K object, one copy, to one miner """
    function_name = sys._getframe().f_code.co_name
    file_path = os.path.join(file_path, "test.txt")
    check_result = put_chunks_base_on_param(bin_path, file_path, 1, 1, 1, 100, 86400, function_name)
    if check_result:
        print("put small file, one copy, successful")
        g_logger.info("put small file, one copy, successful")
    else:
        print("put small file, one copy, failed")
        g_logger.error("put small file, one copy, failed")
    return check_result


def put_big_object_one_copy(bin_path, file_path):
    """ one user put 16M object, one copy, to one miner """
    function_name = sys._getframe().f_code.co_name
    file_path = os.path.join(file_path, "import_file.log")
    check_result = put_chunks_base_on_param(bin_path, file_path, 1, 1, 1, 100, 86400, function_name)
    if check_result:
        print("put big file, one copy, successful")
        g_logger.info("put big file, one copy, successful")
    else:
        print("put big file, one copy, failed")
        g_logger.error("put big file, one copy, failed")
    return check_result


def put_small_object_three_copies(bin_path, file_path):
    """ one user put 128K object, 3 copies, to 3 miner """
    function_name = sys._getframe().f_code.co_name
    file_path = os.path.join(file_path, "test.txt")
    check_result = put_chunks_base_on_param(bin_path, file_path, 1, 3, 3, 100, 86400, function_name)
    if check_result:
        print("put small file, three copy, successful")
        g_logger.info("put small file, three copy, successful")
    else:
        print("put small file, three copy, failed")
        g_logger.error("put small file, three copy, failed")
    return check_result


def put_big_object_three_copies(bin_path, file_path):
    """ one user put 16M object, 3 copies, to 3 miner """
    function_name = sys._getframe().f_code.co_name
    file_path = os.path.join(file_path, "import_file.log")
    check_result = put_chunks_base_on_param(bin_path, file_path, 1, 3, 3, 100, 86400, function_name)
    if check_result:
        print("put big file, three copy, successful")
        g_logger.info("put big file, three copy, successful")
    else:
        print("put big file, three copy, failed")
        g_logger.error("put big file, three copy, failed")
    return check_result


def get_big_object_from_other_user_one_copy(bin_path, file_path):
    """  """
    function_name = sys._getframe().f_code.co_name
    file_path = os.path.join(file_path, "import_file.log")
    check_result = get_chunks_base_on_param(bin_path, file_path, 2, 1, 1, 100, 86400, ownership="other", name=function_name)
    if check_result:
        print("user0 get myself big file, only one user online, successful")
        g_logger.info("user0 get myself big file, only one user online, successful")
    else:
        print("user0 get myself big file, only one user online, failed")
        g_logger.error("user0 get myself big file, only one user online, failed")
    return check_result


def get_big_object_from_myself_two_copies(bin_path, file_path):
    """  """
    function_name = sys._getframe().f_code.co_name
    file_path = os.path.join(file_path, "import_file.log")
    check_result = get_chunks_base_on_param(bin_path, file_path, 2, 2, 2, 100, 86400, ownership="self", name=function_name)
    if check_result:
        print("user0 get myself big file, two user online, successful")
        g_logger.info("user0 get myself big file, two user online, successful")
    else:
        print("user0 get myself big file, two user online, failed")
        g_logger.error("user0 get myself big file, two user online, failed")
    return check_result


def get_object_from_other_user_two_copies(bin_path, file_path):
    """  """
    function_name = sys._getframe().f_code.co_name
    file_path = os.path.join(file_path, "import_file.log")
    check_result = get_chunks_base_on_param(bin_path, file_path, 2, 2, 2, 100, 86400, ownership="other", name=function_name)
    if check_result:
        print("user0 get user1 big file, two user online, successful")
        g_logger.info("user0 get user1 big file, two user online, successful")
    else:
        print("user0 get user1 big file, two user online, failed")
        g_logger.error("user0 get user1 big file, two user online, failed")
    return check_result


def main(argv):
    """ main """
    bin_path = ""  # r"/home/workspace/go/src/github.com/PPIO/go-ppio/bin"
    file_path = ""  # r"/home/workspace/go/src/github.com/PPIO/go-ppio/test_scripts/python_script"

    try:
        opts, args = getopt.getopt(argv, "hb:f:", ["bin_path=", "file_path="])
    except getopt.GetoptError:
        print('main.py --bin_path <bin_path> --file_path <file_path>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py --bin_path <bin_path> --file_path <file_path>')
            sys.exit(2)
        elif opt in ("-b", "--bin_path"):
            bin_path = arg
            if not os.path.exists(bin_path):
                print('action bin file do not exit')
                sys.exit(2)
            else:
                print("bin path: %s" % bin_path)
        elif opt in ("-f", "--file_path"):
            file_path = arg
            if not os.path.exists(file_path):
                print('import file do not exit')
                sys.exit(2)
            else:
                print("file path: %s" % file_path)

    # small_file_path = os.path.join(file_path, "test.txt")
    # big_file_path = os.path.join(file_path, "import_file.log")

    # global g_logger
    # current_time = datetime.datetime.now()
    # timestamp = datetime.datetime.strftime(current_time, "%Y-%m-%d_%H-%M-%S")
    # script_log_path = os.path.join(os.getcwd(), "test_log")
    # if not os.path.exists(script_log_path):
    #     os.makedirs(script_log_path, exist_ok=True)
    # g_logger = set_logger(script_log_path, timestamp)

    # stop_server(miner_clean=True)
    # start_server(start_time="generate_raw_data")
    # start_miner(bin_path, 4, start_time="generate_raw_data")
    # time.sleep(120)
    # stop_server()

    check_result = True
    # check_result &= put_small_object_one_copy(bin_path, file_path)
    # check_result &= put_big_object_one_copy(bin_path, file_path)
    # check_result &= put_small_object_three_copies(bin_path, file_path)
    # check_result &= put_big_object_three_copies(bin_path, file_path)

    check_result &= get_big_object_from_other_user_one_copy(bin_path, file_path)
    # check_result &= get_big_object_from_myself_two_copies(bin_path, file_path)
    # check_result &= get_object_from_other_user_two_copies(bin_path, file_path)
    if check_result:
        print("All cases accomplish, successful")
    else:
        print("All cases accomplish, failed")

    if check_result:
        sys.exit(0)
    else:
        sys.exit(1)


if "__main__" == __name__:
    main(sys.argv[1:])
