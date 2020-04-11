import os,sys,time

import json
import requests
import commands

from kubernetes import client, config
from kubernetes.stream import stream

config.kube_config.load_kube_config(config_file="kubeconfig.yml")

class Testclass:

    kube_api = None

    user0 = None
    user1 = None

    miner0 = None
    miner1 = None
    miner2 = None
    miner3 = None

    ppio_dir = '/home/nfs/go/src/github.com/PPIO/go-ppio'

    shell_command = ['/bin/sh']

    headers = {"Content-Type": "application/x-www-form-urlencoded"} 

    body = {"jsonrpc":"2.0","method":"","params":{},"id":1}

    def __init__(self):
	self.kube_api = client.CoreV1Api()
	self.user0 = self.kube_api.read_namespaced_pod(name='user0', namespace='default')
	self.user1 = self.kube_api.read_namespaced_pod(name='user1', namespace='default')
	self.miner0 = self.kube_api.read_namespaced_pod(name='miner0', namespace='default')
	self.miner1 = self.kube_api.read_namespaced_pod(name='miner1', namespace='default')
 
    def setup(self):
	pass

    def teardown(self):
	pass

    def pod_exec(self,node,commands,namespace='default'):
	'''
	cmds = [
    		"cd /home/workspace/go",
    		"ls",
	]
	self.pod_exec('user0',cmds)
	'''
	ret = '' 

	pod_stream = stream(self.kube_api.connect_get_namespaced_pod_exec, 
				node, 
				namespace,
				command=self.shell_command,
				stderr=True, 
				stdin=True,
				stdout=True, 
				tty=False, 
				_preload_content=False)

	while pod_stream.is_open():
    		pod_stream.update(timeout=3)
    		if pod_stream.peek_stdout():
        		ret = pod_stream.read_stdout()
        		print("STDOUT:\n%s\n" % ret)
    		if pod_stream.peek_stderr():
        		ret = pod_stream.read_stderr()
        		print("STDERR:\n%s\n" % ret)
			break
    		if commands:
        		cmd_item = commands.pop(0)
        		print("Running command... %s\n" % cmd_item)
        		pod_stream.write_stdin(cmd_item + "\n")
    		else:
         		break

	pod_stream.close()

	return ret

    def shell_exec(self,command): 
	status, output = commands.getstatusoutput(command)
	print(output)
	if(status == 0):
		print("command run success\n")
	else:
		print("command run failed\n")
	return status,output

    def rpc_request(self, url, headers, data):
	ret = ''

	response = requests.post(url, data = data, headers = headers);

	if(response.status_code == 200):
		ret = response.text 
		print(ret)
	else:
		print("request failed %s\n" % url)

	return ret
	
    def rpc_call(self,node,command,params,id,node_port):
	#get pod ip
	url = "http://{}:{}".format(node.status.pod_ip,node_port)
	
	#gen post body
	self.body["method"]=command
	self.body["id"]=id
	self.body["params"]=params
	data = json.dumps(self.body)

	#send requests
	mydict = json.loads( self.rpc_request(url, self.headers, data) )

	#get response
	#print(mydict[u'result'][0][u'SegmentInfos'])
	return mydict

    def test(self):
	#object list
	ret = self.rpc_call(self.user0,'ObjectList',[],1,18060)	
	print(ret)

	#object import
	ret = self.rpc_call(self.user0,'ObjectImport',['/home/workspace/video/fg.mp4'],1,18060)
	objhash = ret["result"]

	#check import
	cmds = [
    		"ls /home/regnet-config/master/user0/storage",
	]
	ret = self.pod_exec('user0',cmds)
	objhash_u = objhash.upper()
	assert(ret.find(objhash_u) >= 0)
	
	#object put
	param = []
	param.append(objhash)
	param.append(2)
	param.append(864000)
	param.append(100)
	param.append("public")
	ret = self.rpc_call(self.user0,'ObjectPut',param,1,18060)

	#check put
	time.sleep(30)
	ret = self.rpc_call(self.user0,'ObjectList',[],1,18060)	
	print(ret)
