import os

ratio_path = "D:\\download\\ratio_arrangement.txt"
bi_data_path = "D:\\download\\0b51a878-ddd2-4a9d-9241-b085a7e7c29b.csv"


def collect_ratio_data():
    """ collect ratio data from txt file """
    ratio_dict = dict()
    if os.path.exists(ratio_path):
        with open(ratio_path) as f:
            for line in f.readlines():
                try:
                    ratio_dict.update({line.split()[0]: float(line.split()[1])})
                except IndexError as e:
                    print("ratio data content: %s; exception: %s" % (line, e))
                except ValueError as e:
                    print("ratio data Content: %s; exception: %s" % (line, e))
    return ratio_dict


def collect_bi_data():
    """ collect bi data from csv file """
    bi_dict = dict()
    if os.path.exists(bi_data_path):
        with open(bi_data_path) as f:
            for line in f.readlines():
                if "machine_id" in line or "bw_upload_95" in line:
                    continue
                array = line.strip().split(",")
                try:
                    bi_dict.update({array[1][1:-1]: float(array[4])})
                except ValueError as e:
                    print("BI data content: %s; exception: %s" % (line, e))
    return bi_dict


def comparison_data(ratio_data, bi_data):
    """  """
    # print(ratio_data)
    # print(bi_data)
    ratio_machines = ratio_data.keys()
    bi_machines = bi_data.keys()
    print("Pairatio 统计中有的机器，BI 数据中没有的机器:")
    for machine in ratio_machines:
        if machine not in bi_machines:
            print(machine)
    print("BI 统计中有的机器，Pairatio 数据中没有的机器:")
    for machine in bi_machines:
        if machine not in ratio_machines:
            print(machine)

    comparison_result = dict({"2G": list(), "1G": list(), "500M": list(), "100M": list(), "50M": list(), "<50M": list()})
    for key in ratio_data:
        data = bi_data.get(key, None)
        if data is None:
            continue
        if abs(ratio_data.get(key) - data) > 2 * 1024 * 1024 * 1024:
            comparison_result["2G"].append({"machine": key, "pairatio": ratio_data.get(key), "bi": data})
        elif abs(ratio_data.get(key) - data) > 1 * 1024 * 1024 * 1024:
            comparison_result["1G"].append({"machine": key, "pairatio": ratio_data.get(key), "bi": data})
        elif abs(ratio_data.get(key) - data) > 500 * 1024 * 1024:
            comparison_result["500M"].append({"machine": key, "pairatio": ratio_data.get(key), "bi": data})
        elif abs(ratio_data.get(key) - data) > 100 * 1024 * 1024:
            comparison_result["100M"].append({"machine": key, "pairatio": ratio_data.get(key), "bi": data})
        elif abs(ratio_data.get(key) - data) > 50 * 1024 * 1024:
            comparison_result["50M"].append({"machine": key, "pairatio": ratio_data.get(key), "bi": data})
        else:
            comparison_result["<50M"].append({"machine": key, "pairatio": ratio_data.get(key), "bi": data})
    print("95 带宽差值大于 2G:")
    for info in comparison_result["2G"]:
        print("Machine: %s; pairatio: %s; BI: %s" % (info.get("machine"), info.get("pairatio"), info.get("bi")))
    print("95 带宽差值大于 1G:")
    for info in comparison_result["1G"]:
        print("Machine: %s; pairatio: %s; BI: %s" % (info.get("machine"), info.get("pairatio"), info.get("bi")))
    print("95 带宽差值大于 500M:")
    for info in comparison_result["500M"]:
        print("Machine: %s; pairatio: %s; BI: %s" % (info.get("machine"), info.get("pairatio"), info.get("bi")))
    print("95 带宽差值大于 100M:")
    for info in comparison_result["100M"]:
        print("Machine: %s; pairatio: %s; BI: %s" % (info.get("machine"), info.get("pairatio"), info.get("bi")))
    print("95 带宽差值大于 50M:")
    for info in comparison_result["50M"]:
        print("Machine: %s; pairatio: %s; BI: %s" % (info.get("machine"), info.get("pairatio"), info.get("bi")))
    print("95 带宽差值小于 50M:")
    for info in comparison_result["<50M"]:
        print("Machine: %s; pairatio: %s; BI: %s" % (info.get("machine"), info.get("pairatio"), info.get("bi")))


if __name__ == '__main__':
    ratio_data_dict = collect_ratio_data()
    bi_data_dict = collect_bi_data()
    comparison_data(ratio_data_dict, bi_data_dict)
