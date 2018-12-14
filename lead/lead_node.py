#! /usr/bin/python3

import os
import json
import errno
import strategies

from rpc_api import RPC
from rest_api import REST
from node import Node
from strategies.kodo_encoder import KodoEncoder
from strategies.kodo_decoder import KodoDecoder

from subprocess import call

from tinydb import TinyDB, Query


class LeadNode:
    def __init__(self, config):
        self.config = config
        self._version = config['version']
        self.set_strategy(config['strategy'])
        self.rest = REST(self, config['api_host'],  config['api_port'])
        self.rpc = RPC(self, config['rpc_host'], config['rpc_port'])
        self.db = TinyDB('ledger.json')
        #self.nodes = TinyDB('nodes.json')

    def start(self):
        self.rpc.start()
        self.rest.start()
        self.deploy_all()


    def deploy_all(self):
        call([os.getcwd() + '/deploy.sh'])


    def update_node(self, ip):
        # TODO: Maybe sanitize the ip first ?
        call([os.getcwd() + '/deploy.sh', ip])


    def store(self, filename, file):
        #print('hello')
        #print(self.get_ledger_entries())
        #with open("nodes") as f:
        #    for line in f:
        #        split = line.split(":")
        #        self.nodes[split[0]] = Node(split[0],split[1],split[2],split[3])
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

    #def get_nodes_entries(self):
    #    return list(set(map(
    #        lambda entry: entry['mac'],
    #        self.nodes.search(Query().mac.exists())
    #    )))



if __name__ == '__main__':
    with open('config.json', 'r') as config_file:
        leadNode = LeadNode(json.load(config_file))
        leadNode.start()
