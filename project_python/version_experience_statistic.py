# -*- coding: utf-8 -*-

import datetime


file_size = 1048577  # Units: KB, 1G


def timedelta_to_seconds(start_time, end_time):
    """  """
    if "/" in start_time and ":" in start_time:
        start = datetime.datetime.strptime(start_time, "%Y/%m/%d %H:%M:%S")
        end = datetime.datetime.strptime(end_time, "%Y/%m/%d %H:%M:%S")
        seconds = int((end - start).seconds)
    else:
        start = datetime.datetime.strptime(start_time, "%Y-%m-%d_%H-%M-%S")
        end = datetime.datetime.strptime(end_time, "%Y-%m-%d_%H-%M-%S")
        seconds = int((end - start).seconds)
    return seconds


def speed_cals(seconds):
    return file_size / seconds


def data_statistic(start_list, end_list):
    """  """
    avg_speed = 0
    for start_time, end_time in zip(start_list, end_list):
        seconds = timedelta_to_seconds(start_time, end_time)
        speed = speed_cals(seconds)
        avg_speed += speed
        print("start: %s; end: %s; speed: %s" % (start_time, end_time, str(speed) + " KB/s"))
    avg_speed = avg_speed / len(start_list)
    print("avg speed: %s" % avg_speed + " KB/s")


if "__main__" == __name__:
    start_list = [
"2019/02/01   7:59:17",
"2019/02/01   8:12:44",
"2019/02/01   8:26:20",
"2019/02/01   8:40:11",
"2019/02/01   8:54:09",
"2019/02/01   9:07:53",
"2019/02/01   9:21:26",
"2019/02/01   9:35:10",
"2019/02/01   9:49:33", ]

    end_list = [
"2019/02/01   8:12:44",
"2019/02/01   8:26:20",
"2019/02/01   8:40:11",
"2019/02/01   8:54:09",
"2019/02/01   9:07:53",
"2019/02/01   9:21:26",
"2019/02/01   9:35:10",
"2019/02/01   9:49:33",
"2019/02/01  10:03:41",]

    data_statistic(start_list, end_list)
