from datetime import datetime, timedelta
from influxdb import InfluxDBClient
import os
import sys
import toml


interface_values = "SHOW TAG values FROM \"net\" with key=\"interface\" where host='%s'"
inquery_command = "SELECT * FROM autogen.net WHERE \"host\" = '%s' AND \"interface\" = '%s' AND time >= '%s' AND time <= '%s';"
inquery_robot = "SELECT * FROM autogen.pi_flow_robot WHERE \"host\" = '%s' AND time >= '%s' AND time <= '%s';"
duration_time = 4.5
file_path = "D:\\code\\github\\byq_code\\build_test\\project_python\\work_tools\\config.toml"


def get_all_interface(host_id):
    client = InfluxDBClient("47.114.74.103", 8086, username='admin', password='H!17FHU36pZw&xV3', database="telegraf")
    command = interface_values % host_id
    interface_list = list()
    result_list = client.query(command)
    for result in result_list:
        for i in result:
            interface_list.append(i)
    # print(type(interface_list))
    # print(interface_list)
    return interface_list


def fetch_bandwidth_data(start_time, end_time, host_id, interface="enp2s0f0", robot=0):
    """ fetch bandwidth data from influxdb
    start_time:  eg: 2020-04-15T00:00:00Z
    end_time:    eg: 2020-04-15T00:00:00Z
    robot: 0 - net card flow; 1 - is robot flow
    """
    client = InfluxDBClient("47.114.74.103", 8086, username='admin', password='H!17FHU36pZw&xV3', database="telegraf")
    if robot == 1:
        command = inquery_robot % (host_id, start_time, end_time)
    else:
        command = inquery_command % (host_id, interface, start_time, end_time)
    # print("Influxdb command: %s" % command)
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
        # print("net data: %s" % net_data)
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
    if not raw_data_list:
        return raw_data_list
    if len(raw_data_list) < 2:
        return raw_data_list[0]

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


def statistic_bandwidth_95(data, data_name):
    """  """
    invalid_point_num = 0
    bandwidth_list = list()
    # print("bytes_data 0: %s " % data[0])
    # print("bytes_data %s: %s " % (len(data) - 1, data[-1]))
    for index, bytes_data in enumerate(data):
        # print("bytes_data %s: %s " % (index, bytes_data))
        # print("invalid_point_num", invalid_point_num)
        if index > 287:
            break

        if len(bytes_data) > 0:
            # calc_time = datetime.strptime(bytes_data[0].get("time"), '%Y-%m-%dT%H:%M:%SZ') -\
            #             datetime.strptime(bytes_data[-1].get("time"), '%Y-%m-%dT%H:%M:%SZ')
            # calc_second = calc_time.seconds
            calc_bytes = 0
            calc_result = 0
            calc_second = 300
            if "bytes_sent" in data_name:
                calc_bytes = bytes_data[0].get(data_name) - bytes_data[-1].get(data_name)
                if calc_bytes <= 0:
                    invalid_point_num += 1
                    continue

                if calc_second:
                    # print("calc second is not zone: %s" % bytes_data)
                    calc_result = calc_bytes / calc_second
                else:
                    print("Calc second is zone: %s" % bytes_data)
                    calc_result = 0
            elif "up_bandwidth" in data_name:
                for data in bytes_data:
                    calc_bytes += data.get(data_name)
                calc_result = calc_bytes / len(bytes_data)

            bandwidth_list.append(calc_result * 8 / 1024 / 1024)
        else:
            invalid_point_num += 1
    # print("Valid bandwidth raw data: %s" % bandwidth_list)
    bandwidth_list.sort(reverse=True)
    # print("Valid bandwidth data: %s" % bandwidth_list)
    # print("Bandwidth list len %s" % len(bandwidth_list))
    # print("Invalid point num %s" % invalid_point_num)
    if len(bandwidth_list) > 14:
        bandwidth_95 = bandwidth_list[14]
    elif len(bandwidth_list) == 0:
        bandwidth_95 = 0
    else:
        bandwidth_95 = bandwidth_list[-1]

    valid_divisor = len(bandwidth_list) / 288
    bandwidth_result = bandwidth_95 * valid_divisor

    return bandwidth_95, valid_divisor, bandwidth_result


def read_machine_list(config):
    """ read machine list """
    machine_config = dict()
    if os.path.exists(config):
        machine_config = toml.load(config)
    else:
        print("[Error] Do not have machine list config")
    return machine_config


def generate_bandwidth_time_range(start_time):
    """ Generate bandwidth data sampling time """
    start_hour_minute = datetime.strptime(start_time, '%H:%M')
    start_hour_minute = start_hour_minute - timedelta(seconds=300)
    end_hour_minute = start_hour_minute + timedelta(hours=duration_time, seconds=300)

    start_datetime = datetime(datetime.now().year,
                              datetime.now().month,
                              datetime.now().day,
                              start_hour_minute.hour,
                              start_hour_minute.minute)
    start_datetime_utc = start_datetime - timedelta(hours=8)
    end_datetime = datetime(datetime.now().year,
                            datetime.now().month,
                            datetime.now().day,
                            end_hour_minute.hour,
                            end_hour_minute.minute)
    end_datetime_utc = end_datetime - timedelta(hours=8)

    return start_datetime, end_datetime, start_datetime_utc, end_datetime_utc


def calc_bandwidth(machine_id, start_time, end_time, robot=0):
    """ Calculation bandwidth of 95% value
        robot: 0 - net card flow; 1 - is robot flow
    """
    interface_list = get_all_interface(machine_id)
    sampling_data_list = list()
    if robot == 0:
        data_name = "bytes_sent"
        for interface in interface_list:
            # print(interface)
            data = fetch_bandwidth_data(start_time, end_time, machine_id, interface=interface.get("value"), robot=robot)
            if data:  # 数据为非空,加入统计数据列表
                sampling_data_list.append(data)
        aggregated_data = aggregation_data(sampling_data_list)
    else:
        data_name = "up_bandwidth"
        aggregated_data = fetch_bandwidth_data(start_time, end_time, machine_id, interface="", robot=robot)

    sampling_data = sampling_bandwidth_data(aggregated_data, end_time)
    bandwidth_95, valid_divisor, bandwidth_result = statistic_bandwidth_95(sampling_data, data_name)
    # earning = bandwidth_result / 1024 / 31 * 3000

    # print("interface list: %s" % interface_list)
    # print("bandwidth_95, valid_divisor, bandwidth_result", bandwidth_95, valid_divisor, bandwidth_result)
    # print("earning sum: %s" % earning)
    return bandwidth_95


def calc_single_machine_bandwidth(machine_id, start_time):
    """ Calculation single machine bandwidth """
    print("Machine id: %s" % machine_id)

    start_datetime, end_datetime, start_datetime_utc, end_datetime_utc = generate_bandwidth_time_range(start_time)
    start_shanghai = start_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_shanghai = end_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
    start_utc = start_datetime_utc.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_utc = end_datetime_utc.strftime('%Y-%m-%dT%H:%M:%SZ')
    print("Check bandwidth time range(Shanghai): %s, %s" % (start_shanghai, end_shanghai))
    print("Check bandwidth time range(UTC): %s, %s" % (start_utc, end_utc))

    bandwidth_95 = calc_bandwidth(machine_id, start_utc, end_utc)
    robot_bandwidth_95 = calc_bandwidth(machine_id, start_utc, end_utc, robot=1)
    return start_shanghai, end_shanghai, bandwidth_95, robot_bandwidth_95


def main(config_file):
    config = read_machine_list(config=config_file)
    statistic_dict = dict()
    expect_dict = dict()
    for machine in config:
        expect_bandwidth = int(config.get(machine).get("expect_bandwidth")) / 1000000
        result = calc_single_machine_bandwidth(machine, config.get(machine).get("daily_begin"))
        statistic_dict.update({machine: result})
        expect_dict.update({machine: expect_bandwidth})

    for key in statistic_dict:
        bandwidth_95 = statistic_dict.get(key)[2]
        robot_bandwidth_95 = statistic_dict.get(key)[3]
        expect_result = expect_dict.get(key)
        reason = ""
        if robot_bandwidth_95 == 0:
            if bandwidth_95 < expect_result:
                reason += "\033[1;31m 机器人打量异常 \033[0m "
            else:
                reason += "\033[1;32m 流量已达到预期，机器人未工作 \033[0m "
        else:
            if bandwidth_95 > expect_result:
                reason += "\033[1;31m 机器人打量过多 \033[0m "
            elif bandwidth_95 / expect_result < 0.8:
                reason += "\033[1;33m 机器人打量不足 \033[0m "
            else:
                reason += "\033[1;32m 机器人打量正常 \033[0m"

        txt = "machine id: %s; robot work time range(Shanghai) %s, %s; bandwidth 95: %s; robot 95: %s; summary: %s \n"
        print(txt % (key,
                     statistic_dict.get(key)[0],
                     statistic_dict.get(key)[1],
                     statistic_dict.get(key)[2],
                     statistic_dict.get(key)[3],
                     reason))


if __name__ == "__main__":
    params = sys.argv[1:]
    if len(params) == 1:
        config_file_name = sys.argv[1]
        current_path = os.path.abspath(os.path.dirname(__file__))
        config_file = os.path.join(current_path, config_file_name)
        main(config_file)
    else:
        exit(1)
