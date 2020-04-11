# -*- coding: utf-8 -*-

import time
from xmlrpc import client
from robot.api import logger
from manager import Manager


class SupervisorController(Manager):
    """ Supervisor controller """

    def __init__(self, config):
        """ Init
        Args:
            node: node instance
        """
        super(SupervisorController, self).__init__(config)

    def create_server_connect(self, process_name):
        """ Create server connect """
        server = None
        server_name = str()
        node_config = self.config.get_config(process_name)
        logger.info("Process name: %s; config: %s" % (process_name, node_config), html=True, also_console=True)
        if node_config:
            ip = node_config.get("ip", "127.0.0.1")
            port = 9001
            url = "http://%s:%s/RPC2" % (ip, port)
            server = client.ServerProxy(url)
            server_name = node_config.get("name", "")
        else:
            logger.error("Can not get node config for create server connect", html=True)

        if server:
            try:
                state = server.supervisor.getState()
                if state.get("statecode") != 1:
                    server = None
            except Exception as e:
                server = None
                logger.error("Supervisor remote connect error:%s" % e, html=True)
            else:
                logger.info("Supervisor remote connect successful.", html=True, also_console=True)

        return server, server_name

    def get_status(self, process_name):
        """ Fetch process status """
        state = str()
        server, server_name = self.create_server_connect(process_name)
        if server and server_name:
            try:
                process_info = server.supervisor.getProcessInfo(server_name)
                if process_info:
                    state = process_info.get("statename", "")
            except client.Error as e:
                logger.error("Fetch process %s info error %s" % (server_name, e), html=True)
        return state

    def start_process(self, process_name):
        """ Start process """
        ret = False
        server, server_name = self.create_server_connect(process_name)
        if server and server_name:
            try:
                server.supervisor.startProcess(server_name)
                for i in range(3):
                    time.sleep(5)
                    state = self.get_status(process_name)
                    logger.info("Process %s state: %s" % (server_name, state), html=True, also_console=True)
                    if state == "RUNNING":
                        ret = True
                        break
            except client.Error as e:
                logger.info("Start process %s error %s" % (server_name, e), html=True)

        return ret

    def stop_process(self, process_name):
        """ Stop process """
        ret = False
        server, server_name = self.create_server_connect(process_name)
        if server and server_name:
            try:
                server.supervisor.stopProcess(server_name)
                for i in range(3):
                    time.sleep(5)
                    state = self.get_status(process_name)
                    logger.info("Process %s state: %s" % (server_name, state), html=True, also_console=True)
                    if state == "STOPPED":
                        ret = True
                        break
            except client.Error as e:
                logger.info("Stop process %s error %s" % (server_name, e), html=True)

        return ret
