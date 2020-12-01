import requests
from datetime import datetime, timedelta


def get_platform_data():
    """ Fetch all node data include specific tasks and docker numbers from platform """
    url = "https://api.paigod.work/v1/device/list"
    param = {
        "pageIndex": 1,
        'state': 'billing,taskDeployed',
        'online': 'online',
        "pageSize": 1000}
    headers = {
        "Authorization": "Bearer eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjMxMCwidXNlcm5hbWUiOiLmtL7kupHnrqHnkIYiLCJyb2xlIjoxfQ.QNLs8AMmiD8_mNnii6zBeW-j3x2KekWLRfA6s0gJE5uPqBzKTDMq_xfI0j5l5s3953SasC8WeCHeglpzTH4OOixVTcf0xe9iuxnrR-YeS3gvEMzVb2fo8XhM8wgRGekRHLuzUnNer1lWBgVxACYwBRkTFnUZPdBiAt1mECVEXTmkiaWvIxjZblLksVk4-a1TB7drBAnWQRqP83tNzmYZ8G_acQFEF6MyJ4aSgTCPpNW7qkGptPt3lIFgzIGYOpM-KLzppv-tkuSGDwAgYVSV4gIQsjTzheBWotwZmu5AAmbYYBFzBOdSzl4DXCW6b66_ecIlGSYfpK1laB2YbQxIog"}
    request = requests.get(
        url,
        params=param,
        headers=headers)
    print("request.status_code:", request.status_code)
    print("request.raw", request.raw)
    response = request.json()
    return response


def node_amendment_bandwidth(platform_data):
    """ min(report_bandwidth, press_test_bandwidth) is amendment bandwidth """
    max_test = platform_data.get("maxTestUpBandwidth", 0)
    avg_test = platform_data.get("avgTestUpBandwidth", 0)
    report_bandwidth = platform_data.get("upBandwidthPerLine", 0) * platform_data.get("lineCount", 0)
    press_test_bandwidth = max_test if max_test != 0 else avg_test
    if report_bandwidth != 0 and press_test_bandwidth != 0:
        amendment_bandwidth = press_test_bandwidth if report_bandwidth > press_test_bandwidth else report_bandwidth
    else:
        amendment_bandwidth = report_bandwidth if report_bandwidth != 0 else press_test_bandwidth
    return amendment_bandwidth


def statistic_bandwidth(platform_data, task_name, is_docker):
    """ Statistic bandwidth """
    task_node_number = 0
    tasks_bandwidth_total = 0
    for node_data in platform_data:
        bind_time = datetime.fromtimestamp(node_data.get("bindTime")).date()
        if datetime.now().date() - bind_time < timedelta(1):
            continue
        if task_name in node_data.get("specificTasks"):
            amendment_bandwidth = node_amendment_bandwidth(node_data)
            device_id = node_data.get("deviceUUID")
            if is_docker:
                line_count = node_data.get("lineCount", 0)
                base_bandwidth = amendment_bandwidth / line_count if line_count != 0 else amendment_bandwidth
                docker_number = 0
                for task_info in node_data.get("tasks"):
                    if task_info is not None and task_info.get("name") == task_name:
                        docker_number += task_info.get("realDockerNumber", 0)
                # docker_number = sum([i.get("realDockerNumber", 0) for i in node_data.get("tasks") if i is not None and i.get("name") == task_name])
                task_bandwidth = base_bandwidth * docker_number
            else:
                task_bandwidth = amendment_bandwidth
            txt = "ID: %s; task: %s; state: %s; network state: %s; bindtime: %s; task bandwidth: %s"
            print(txt % (device_id, task_name, node_data.get("state"), node_data.get("online"),
                         bind_time.strftime("%Y-%m-%d"), task_bandwidth))
            task_node_number += 1
            tasks_bandwidth_total += task_bandwidth
    tasks_bandwidth_total = tasks_bandwidth_total / 1024 / 1024 / 1024
    print("Task: %s; node number: %s; task bandwidth total: %s" % (task_name, task_node_number, tasks_bandwidth_total))


if __name__ == '__main__':
    data = get_platform_data()
    # statistic_bandwidth(data.get("devices", dict()), "daai", False)
    # statistic_bandwidth(data.get("devices", dict()), "kuaishou", False)
    # statistic_bandwidth(data.get("devices", dict()), "bz", False)
    # statistic_bandwidth(data.get("devices", dict()), "hcdne", True)
    # statistic_bandwidth(data.get("devices", dict()), "hcdne", True)
    # statistic_bandwidth(data.get("devices", dict()), "yunfan", True)
    # statistic_bandwidth(data.get("devices", dict()), "kcsm", True)
    # statistic_bandwidth(data.get("devices", dict()), "kcs", True)
    statistic_bandwidth(data.get("devices", dict()), "bdcd", True)
