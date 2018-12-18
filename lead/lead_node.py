#! /usr/bin/python3

import os
import sys
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
    def __init__(self, config, test=False):
        if test:
            config['api_host'] = 'localhost'
            config['rpc_host'] = 'localhost'

        self.config = config
        self._version = config['version']
        self.nodes = {}
        self.rest = REST(self, config['api_host'],  config['api_port'])
        self.rpc = RPC(config['rpc_host'], config['rpc_port'])
        self.set_strategy(config['strategy'])
        # Disable the query cache because we have two instances open!
        db = TinyDB('db.json')
        self.nodes_db = db.table('nodes', cache_size=0)
        self.ledger_db = db.table('ledger', cache_size=0)


    def start(self):
        Timer(1, self.sync_nodes).start() # Run every 2 seconds
        self.rpc.start()
        self.rest.start()
        self.deploy_all()


    # This runs in a thread and watches for new DB entries
    def sync_nodes(self):
        print("[*] Syncing nodes...")
        # Force reload the DB cause fuck it we're desperate now
        # db = TinyDB('db.json')
        # self.nodes_db = db.table('nodes', cache_size=0)
        for node in self.nodes_db.all():
            if node['mac'] not in self.nodes:
                for key, node in self.nodes.items():
                    node.propagate(node['mac'], node['ip'], node['port'], node['units'])

                # Will replace
                print("[*] Adding node {} to the list".format(node['ip']))
                self.nodes[node['mac']] = Node(node['mac'], node['ip'],
                                               node['port'], node['units'])

        Timer(1, self.sync_nodes).start() # Run every 2 seconds


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
    debug = (len(sys.argv) > 1 and sys.argv[1] == '--debug')
    with open('config.json', 'r') as config_file:
        leadNode = LeadNode(json.load(config_file), debug)
        leadNode.start()
