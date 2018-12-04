#! /usr/bin/python3

import os
import json
import errno
import strategies

from node import Node
from rpc_api import RPC
from rest_api import REST

from subprocess import call

from tinydb import TinyDB, Query


class LeadNode:
    def __init__(self, config):
        self.config = config
        self._version = config['version']
        self.nodes = {}
        self.rest = REST(self, config['api_host'],  config['api_port'])
        self.rpc = RPC(self, config['rpc_host'], config['rpc_port'])
        self.set_strategy(config['strategy'])
        self.db = TinyDB('ledger.json')


    def start(self):
        self.rpc.start()
        self.rest.start()
        self.deploy_all()


    def add_node(self, ip, mac, port, units):
        for mac, node in self.nodes.items():
            node.propagate(mac, ip, port, units)

        # Will replace
        self.nodes[mac] = Node(mac, ip, port, units)


    def deploy_all(self):
        call([os.getcwd() + '/deploy.sh'])


    def update_node(self, ip):
        # TODO: Maybe sanitize the ip first ?
        call([os.getcwd() + '/deploy.sh', ip])


    def store(self, filename, file):
        return self.strategy.store_file(file, filename)


    def retrieve(self, file_name):
        locations = map(
            lambda entry: entry['location'],
            self.db.search(Query().file_name == file_name)
        )
        return self.strategy.retrieve_file(file_name, locations)


    def set_strategy(self, choice):
        self.strategy = strategies.get(
            choice,
            self,
            **self.config['strategies'][choice]
        )


    def add_to_ledger(self, file_name, location):
        self.db.insert({'file_name': file_name, 'location': location})


    def get_ledger_entries(self):
        return list(set(map(
            lambda entry: entry['file_name'],
            self.db.search(Query().file_name.exists())
        )))



if __name__ == '__main__':
    with open('config.json', 'r') as config_file:
        leadNode = LeadNode(json.load(config_file))
        leadNode.start()
