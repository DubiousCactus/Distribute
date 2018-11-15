#! /usr/bin/python3

import os
import json
import errno
import strategies

from node import Node
from rpc_api import RPC
from rest_api import REST

from subprocess import call


class LeadNode:
    def __init__(self, config):
        self.config = config
        self._version = config['version']
        self.nodes = {}
        self.rest = REST(self, config['api_host'],  config['api_port'])
        self.rpc = RPC(self, config['rpc_host'], config['rpc_port'])
        self.set_strategy(config['strategy'])

    def start(self):
        self.rest.start()
        self.rpc.start()

    def add_node(self, ip, mac, port, units):
        # Will replace
        self.nodes[mac] = Node(mac, ip, port)

    def update_node(self, ip):
        # TODO: Maybe sanitize the ip first ?
        call(['deploy.sh', ip])

    def store(self, file):
        self.strategy.store_file(file)

    def set_strategy(self, choice):
        self.strategy = strategies.get(
            choice,
            **self.config['strategies'][choice]
        )


if __name__ == '__main__':
    with open('config.json', 'r') as config_file:
        leadNode = LeadNode(json.load(config_file))
        leadNode.start()
