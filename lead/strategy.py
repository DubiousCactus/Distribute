from abc import ABC, abstractmethod
import json

#This class is abstract and ment to act according to the the config.json
class Strategy:
    @abstractmethod
    def __init__(self, nodes, config):
        self.nodes = nodes
        self.strategy = config['strategy']
        self.coding = coding['strategies'][strategy]['coding']
        self.replicas = coding['strategies'][strategy]['coding']
        self.losses = coding['strategies'][strategy]['coding']

    @abstractmethod
    def execute(self):
        print('Not yet implmented')

