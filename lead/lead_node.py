#! /usr/bin/python3

import os
import json
import errno
import rpc_api
import rest_api

from node import Node
from subprocess import call

app = Flask(__name__)

class LeadNode:
    def __init__(self, config):
        self._version = config['version']
        self.nodes = []
        self.rest = rest_api(self, config['api_host'],  config['api_port'])
        self.rpc = rest_api(self, config['rpc_host'], config['rpc_port'])

    def start(self):
        self.rest.start()
        self.rpc.start()

    def updateCodeOnSlave(self, ip):
        # TODO: Maybe sanitize the ip first ?
        call(['deploy.sh', ip])



if __name__ == '__main__':
    with open('config.json', 'r') as config_file:
        leadNode = LeadNode(config_file)
        leadNode.start()
