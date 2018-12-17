#! /usr/bin/python3

import os
import time
import json
import errno
import strategies

from node import Node
from rpc_api import RPC
from rest_api import REST

from threading import Timer
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
        # Disable the query cache because we have two instances open!
        self.nodes_db = TinyDB('nodes.json', cache_size=0)
        self.ledger_db = TinyDB('ledger.json', cache_size=0)


    def start(self):
        self.rpc.start()
        self.rest.start()
        self.deploy_all()
        Timer(2, self.sync_nodes) # Run every 2 seconds


    # This runs in a thread and watches for new DB entries
    def sync_nodes(self):
        for node in self.nodes_db.all():
            if not self.nodes.has_key(node['mac']):
                for key, node in self.nodes.items():
                    node.propagate(node['mac'], node['ip'], node['port'], node['units'])

                # Will replace
                self.nodes[mac] = Node(mac, ip, port, units)

        Timer(2, self.sync_nodes) # Run every 2 seconds


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
            self.ledger_db.search(Query().file_name == file_name)
        )
        return self.strategy.retrieve_file(file_name, locations)


    def set_strategy(self, choice):
        self.strategy = strategies.get(
            choice,
            self,
            **self.config['strategies'][choice]
        )


    def get_ledger_entries(self):
        return list(set(map(
            lambda entry: entry['file_name'],
            self.ledger_db.search(Query().file_name.exists())
        )))



if __name__ == '__main__':
    with open('config.json', 'r') as config_file:
        leadNode = LeadNode(json.load(config_file))
        leadNode.start()
