from datetime import datetime, timedelta
from influxdb import InfluxDBClient
import pytz
import time

local_tz = pytz.timezone('Asia/Shanghai')
# client = InfluxDBClient("47.114.74.103", 8086, username='admin', password='H!17FHU36pZw&xV3', database="telegraf")
# list_measurements = client.get_list_measurements()
# for m in list_measurements:
#     print(m)

# command = "SELECT * FROM five_minutes.net_5m WHERE \"host\" = '6630e6ad4cf649f1a1329366bf8862f1' AND time >= %ss AND time <= %ss;"
# command = "SELECT * FROM five_minutes.net_5m WHERE \"host\" = '6630e6ad4cf649f1a1329366bf8862f1' AND time >= '%s' AND time <= '%s';"
# command = "SELECT * FROM autogen.net WHERE \"host\" = '9c49383d3e5947efaadd2284ae6fd6e2' AND time >= '%s' AND time <= '%s' GROUP BY \"interface\";"
# command = command % ("2020-04-22T00:00:00Z", "2020-04-22T23:59:00Z")
# command = "select non_negative_derivative(last(bytes_sent), 1s) from one_minute.net_1m where \"host\"='6630e6ad4cf649f1a1329366bf8862f1' AND time >= '%s' AND time <= '%s' GROUP BY time(5m);"
# command = "SELECT * FROM one_minute.net_1m WHERE \"host\" = '6630e6ad4cf649f1a1329366bf8862f1'  AND time >= '%s' AND time <= '%s';"
# tz('Asia/Shanghai')
# command = command % ("2020-04-25T15:59:00Z", "2020-04-26T15:59:00Z")
# print(command)
# info = list(client.query(command))
# net_data = list()
# for content in info:
#     for line in content:
#         net_data.append(line)
#         print(line)


# command = "SELECT * FROM net WHERE \"host\" = '6630e6ad4cf649f1a1329366bf8862f1' AND time >= '%s' AND time <= '%s';"
start_timestamp = int(time.mktime(datetime.strptime("2020-04-25 23:59:00", '%Y-%m-%d %H:%M:%S').astimezone(local_tz).timetuple()))
end_timestamp = int(time.mktime(datetime.strptime("2020-04-27 23:59:00", '%Y-%m-%d %H:%M:%S').astimezone(local_tz).timetuple()))
# command = command % (start_timestamp, end_timestamp)
# command = "SELECT * FROM five_minutes.net_5m WHERE \"host\" = '6630e6ad4cf649f1a1329366bf8862f1' AND time >= 1587830340s AND time <=1587916740s ;"
# print(command)
# info = list(client.query(command))
# net_data = list()
# for content in info:
#     for line in content:
#         net_data.append(line)
#         print(line)

# all_m = list(client.query("show measurements;"))
# for n in all_m:
#     print(n)

interface_values = "SHOW TAG values FROM \"net\" with key=\"interface\" where host='%s'"
inquery_command = "SELECT * FROM autogen.net WHERE \"host\" = '%s' AND \"interface\" = '%s' AND time >= '%s' AND time <= '%s';"  # GROUP BY time(5m);
# inquery_command = "SELECT * FROM \"net\" WHERE \"host\" = '6630e6ad4cf649f1a1329366bf8862f1' AND time >= '%s' AND time <= '%s';"
# inquery_command = "SELECT * FROM \"net_5m\" WHERE \"host\" = '6630e6ad4cf649f1a1329366bf8862f1';"


def get_all_interface(host_id):
    client = InfluxDBClient("47.114.74.103", 8086, username='admin', password='H!17FHU36pZw&xV3', database="telegraf")
    command = interface_values % host_id
    interface_list = list()
    result_list = client.query(command)
    for result in result_list:
        for i in result:
            interface_list.append(i)
    # print(type(interface_list))
    print(interface_list)
    return interface_list


def fetch_bandwidth_data(start_time, end_time, host_id, interface="enp2s0f0"):
    """ fetch bandwidth data from influxdb
    start_time:  eg: 2020-04-15T00:00:00Z
    end_time:    eg: 2020-04-15T00:00:00Z
    """
    client = InfluxDBClient("47.114.74.103", 8086, username='admin', password='H!17FHU36pZw&xV3', database="telegraf")
    command = inquery_command % (host_id, interface, start_time, end_time)
    print("Influxdb command: %s" % command)
    info = list(client.query(command))
    net_data = list()
    for content in info:
        for line in content:
            net_data.insert(0, line)
            # print(line)

    return net_data


def sampling_bandwidth_data(net_data, end_time, time_interval=300):
    """ Statistic bandwidth of 95 peak """
    index = 0
    bandwidth_sampling = list()  # 将一段时间数据，分组存储
    cache = list()
    if not net_data:
        print("net data: %s" % net_data)
        return bandwidth_sampling

    time_string = net_data[0].get("time") if len(net_data) > 0 else ""
    try:
        time_datetime = datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError as e:
        print("time datetime: %s" % time_string)
        print("net data: %s" % net_data)
        raise e
    sampling_datetime = time_datetime - timedelta(seconds=time_interval)
    while index < len(net_data):
        # print(sampling_datetime)
        date_time = datetime.strptime(net_data[index].get("time"), '%Y-%m-%dT%H:%M:%SZ')
        pack = True if date_time <= sampling_datetime else False  # 时间比较, 达到采样时间间隔后，更新采样时间段

        if pack:  # 达到采样时间间隔后，将该时间段数据作为一组数据，存储到数据列表中
            if date_time <= sampling_datetime:  # 数据时间点 <= 采样时间边界，需要记录数据到本时间段内，否则记录到下一时间段
                cache.append(net_data[index])
                bandwidth_sampling.append(cache)
            else:
                pass
            # bandwidth_sampling.append(cache)
            cache = list()
            sampling_datetime -= timedelta(seconds=time_interval)
        else:
            cache.append(net_data[index])
            index += 1

    bandwidth_sampling.append(cache)  # 存储最后一组数据

    return bandwidth_sampling


def aggregation_data(raw_data_list):
    """  """
    if len(raw_data_list) < 2:
        return raw_data_list

    last_data_len = len(raw_data_list[-1])
    for index in range(len(raw_data_list) - 1):
        for data_index in range(len(raw_data_list[index])):
            data_time = datetime.strptime(raw_data_list[index][data_index].get("time"), '%Y-%m-%dT%H:%M:%SZ')
            if last_data_len > data_index:
                raw_time = datetime.strptime(raw_data_list[-1][data_index].get("time"), '%Y-%m-%dT%H:%M:%SZ')
                if abs(raw_time - data_time) < timedelta(seconds=60):
                    raw_data_list[-1][data_index]["bytes_recv"] += raw_data_list[index][data_index].get("bytes_recv")
                    raw_data_list[-1][data_index]["bytes_sent"] += raw_data_list[index][data_index].get("bytes_sent")
            else:
                raw_data_list[-1].append(raw_data_list[index][data_index])
    return raw_data_list[-1]


def statistic_bandwidth_95(data):
    """  """
    invalid_point_num = 0
    bandwidth_list = list()
    print("bytes_data 0: %s " % data[0])
    print("bytes_data %s: %s " % (len(data) - 1, data[-1]))
    for index, bytes_data in enumerate(data):
        print("bytes_data %s: %s " % (index, bytes_data))
        print("invalid_point_num", invalid_point_num)
        if index > 287:
            break

        if len(bytes_data) > 0:
            # calc_time = datetime.strptime(bytes_data[0].get("time"), '%Y-%m-%dT%H:%M:%SZ') -\
            #             datetime.strptime(bytes_data[-1].get("time"), '%Y-%m-%dT%H:%M:%SZ')
            # calc_second = calc_time.seconds
            calc_second = 300
            calc_bytes = bytes_data[0].get("bytes_sent") - bytes_data[-1].get("bytes_sent")

            if calc_bytes <= 0:
                invalid_point_num += 1
                continue

            if calc_second:
                # print("calc second is not zone: %s" % bytes_data)
                calc_result = calc_bytes / calc_second
            else:
                print("Calc second is zone: %s" % bytes_data)
                calc_result = 0
            bandwidth_list.append(calc_result * 8 / 1024 / 1024)
        else:
            invalid_point_num += 1
    print("Valid bandwidth raw data: %s" % bandwidth_list)
    bandwidth_list.sort(reverse=True)
    print("Valid bandwidth data: %s" % bandwidth_list)
    print("Bandwidth list len %s" % len(bandwidth_list))
    print("Invalid point num %s" % invalid_point_num)
    if len(bandwidth_list) > 14:
        bandwidth_95 = bandwidth_list[14]
    else:
        bandwidth_95 = 0

    valid_divisor = len(bandwidth_list) / 288
    bandwidth_result = bandwidth_95 * valid_divisor

    return bandwidth_95, valid_divisor, bandwidth_result

int()
def main():
    start = "2020-05-11T15:59:00Z"  # UTC0, UTC8:2020-04-25T23:59:00Z
    end = "2020-05-12T15:59:59Z"    # UTC0, UTC8:2020-04-26T23:59:00Z
    host_id = "6630e6ad4cf649f1a1329366bf8862f1"
    interface_list = get_all_interface(host_id)
    sampling_data_list = list()
    for interface in interface_list:
        # print(interface)
        data = fetch_bandwidth_data(start, end, host_id, interface=interface.get("value"))
        if data:  # 数据为非空,加入统计数据列表
            sampling_data_list.append(data)

    aggregated_data = aggregation_data(sampling_data_list)
    sampling_data = sampling_bandwidth_data(aggregated_data, end)
    bandwidth_95, valid_divisor, bandwidth_result = statistic_bandwidth_95(sampling_data)
    earning = bandwidth_result / 1024 / 31 * 3000

    print("interface list: %s" % interface_list)
    print("bandwidth_95, valid_divisor, bandwidth_result", bandwidth_95, valid_divisor, bandwidth_result)
    print("earning sum: %s" % earning)


if __name__ == "__main__":
    main()
    pass
