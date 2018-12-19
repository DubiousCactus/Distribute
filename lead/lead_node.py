import os
import json
import errno
import strategies

from rpc_api import RPC
from rest_api import REST
from strategies.slave_to_slave_coded import Slave_to_slave_coded
from strategies.slave_to_slave_replica import Slave_to_slave_replica
from strategies.master_to_slave_coded import Master_to_slave_coded
from strategies.master_to_slave_replica import Master_to_slave_replica

from subprocess import call

from tinydb import TinyDB, Query


class LeadNode:
    def __init__(self, config):
        self.config = config
        self._version = config['version']
        self.strategy = None
        self.db = TinyDB('ledger.json')
        self.set_strategy(config['strategy'],1)
        self.rest = REST(self, config['api_host'],  config['api_port'])
        self.rpc = RPC(self, config['rpc_host'], config['rpc_port'])

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
        return self.strategy.store_file(file, filename)


    def retrieve(self, file_name):
        locations = map(
            lambda entry: entry['location'],
            self.db.search(Query().file_name == file_name)
        )
        return self.strategy.retrieve_file(file_name, locations)


    def set_strategy(self, choice, att):
        if str(choice) == "master_to_slave_replica":
            self.strategy = Master_to_slave_replica(self,"master_to_slave_replica with {} replications".format(att,slice), att)
        if str(choice) == "slave_to_slave_replica":
            self.strategy = Slave_to_slave_replica(self,"slave_to_slave_replica with {} replication".format(att,slice), att)
        if str(choice) == "master_to_slave_coded":
            self.strategy = Master_to_slave_coded(self,"master_to_slave_coded with {} loses".format(att),att)
        if str(choice) == "slave_to_slave_coded":
            self.strategy = Slave_to_slave_coded(self,"slave_to_slave_coded with {} loses".format(att),att)
        #        self.strategy = strategies.get(
#            choice,
#            self,
#            **self.config['strategies'][choice]
#        )

    def getstrategies(self):
        return list(self.config['strategies'].keys())


    def getcurrentStrategy(self):
        if self.strategy is None:
            return ""
        return "{}".format(self.strategy.description)


    def add_to_ledger(self, file_name, location,size):
        self.db.insert({'file_name': file_name, 'location': location,'size':size})


    def get_ledger_entries(self):
        return list(set(map(
            lambda entry: entry['file_name'],
            self.db.search(Query().file_name.exists())
        )))


if __name__ == '__main__':
    with open('config.json', 'r') as config_file:
        leadNode = LeadNode(json.load(config_file))
        leadNode.start()
