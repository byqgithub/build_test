# Single Regnet User Manual
|Author | Ver | Time | Description |
| ----- | --- | -----------| ---------------|
|Qiyu   | 0.1 |2019/01/15  | Initial version|


<!-- TOC -->
<!-- /TOC -->

# 1. 设计目标
1. 检测holder账户是否正确。


# 2. 测试环境搭建
该测试需要访问AWS生产环境中Mysql环境，因此需要运行在ES2上部署，操作系统类似于centos。

```bash
# 1. 在 /home 目录下，创建 workspace 目录；
> cd /home/
> mkdir workspace
# 2. 复制测试脚本和配置文件到 workspace 目录
# 3. 检测python环境
> python --version
# 4. 安装并更新pip
  如果python版本是2.7：
> sudo yum -y install python-pip
> sudo pip install --upgrade pip
  如果python版本是2.7：
> sudo yum -y install python3-pip
> sudo pip install --upgrade pip
# 5. 安装python mysql库
> sudo pip install pymysql
```

# 3. 脚本使用
1. 参数介绍：

   --config_file:    配置文件路径（支持相对路径）

   --result_output:  结果输出路径（支持相对路径）
```bash
# 如果在脚本所在目录下执行，例子如下：
python check_holder_account.py --config_file=./config.json --result_output=./result
```
2. 配置文件说明：
```bash
{
  "mysql": {
      "host": "172.172.0.11",   # mysql 服务内网IP
      "port": 3306,
      "user": "root",           # mysql 账号
      "password": "168168",     # mysql 密码
      "db": "ppio"
  },
  "rpc": {
      "internal": 1,
      "timeout": 5,
      "headers": {
          "Content-Type": "text/json"
      }
  },
  "ppio_chain": [
      {
          "ip": "127.0.0.1",   # 链服务内网IP
          "port": 8685         # 链服务端口
      }
  ]
}
```
# 4. 定时任务设置
```bash
# 脚本在每晚23：30执行检查，利用crontab定时任务实现；
# 例：脚本路径为/home/workspace
> crontab -e
> 30 23 * * * python /home/workspace/check_holder_account.py --config_file=/home/workspace/config.json --result_output=/home/workspace/result
```
# 5. 结果查看
1. 测试结果路径：测试报告存放于 result_output 目录下的csv文件中。