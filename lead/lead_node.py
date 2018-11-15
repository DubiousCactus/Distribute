#! /usr/bin/python3

import os
import json
import errno

from rest_api import REST
from rpc_api import RPC
from node import Node
from subprocess import call

class LeadNode:
    def __init__(self, config):
        self._version = config['version']
        self.nodes = {}
        self.rest = REST(self, config['api_host'],  config['api_port'])
        self.rpc = RPC(self, config['rpc_host'], config['rpc_port'])

    def start(self):
        self.rest.start()
        self.rpc.start()

    def addNode(self, ip, mac, port, units):
        # Will replace
        self.nodes[mac] = Node(mac, ip, port)

    def updateNode(self, ip):
        # TODO: Maybe sanitize the ip first ?
        call(['deploy.sh', ip])

    def store(self, file):
        pass


if __name__ == '__main__':
    with open('config.json', 'r') as config_file:
        leadNode = LeadNode(json.load(config_file))
        leadNode.start()
