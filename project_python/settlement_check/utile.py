# -*- coding: utf-8 -*-


import logging
from settlement_check.constant import Constant


def id_to_name(member_id=str()):
    """ ID converter to name

    Args:
        member_id: ID
    """
    try:
        member_id = member_id.strip()
        if member_id in Constant.NAME_ID.keys():
            return member_id

        if member_id:
            return Constant.ID_NAME[member_id]
        else:
            return ''
    except KeyError:
        g_logger.exception("converter parameter error, do not in member list")


def name_to_id(name=str()):
    """ Name converter to id

        Args:
            name: name
    """
    try:
        name = name.strip()
        if name in Constant.ID_NAME.keys():
            return name

        if name:
            return Constant.NAME_ID[name]
        else:
            return ''
    except KeyError:
        g_logger.exception("converter parameter error, do not in member list")


def set_logger():
    """ Set logger system """
    logger_name = 'Settlement'
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    log_path = Constant.LOG_PATH
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    log_format = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
    data_format = "%a %d %b %Y %H:%M:%S"
    formatter = logging.Formatter(log_format, data_format)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


g_logger = set_logger()
