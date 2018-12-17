#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#
# Distributed under terms of the MIT license.

"""
Master to slave using replication
"""

from . import Strategy
from random import shuffle

class Master_to_slave_replica(Strategy):
    def __init__(self, this_controller, desc, nb_replicas):
        Strategy.__init__(self, this_controller, desc)
        self.description = desc
        self.nb_replicas = nb_replicas
        self.controller = this_controller
        self.nodes = []


    def store_file(self, file_bytes, file_name):
        self.nodes = Strategy(Master_to_slave_replica,self).getNodes()
        shuffle(self.nodes)
        shuffle(self.nodes)
        print("replications {}".format(self.nb_replicas))
        print("number of nodes: {}".format(len(self.nodes)))
        if not self.nodes:
            return False
        i = 0
        for n in range(self.nb_replicas):
            if i > self.nb_replicas or i >= len(self.nodes):
                break;
            print(file_name)
            response = self.nodes[i].write(file_name,file_bytes)
            if response and response["result"]["code"] == 200:
                print("file uploaded to {}".format(self.nodes[i].mac))
                self.controller.add_to_ledger(file_name, self.nodes[i].mac)
                i = i + 1
            else:
                # If a node can't be written to, it should be considered fatal
                return False
        return True


    def retrieve_file(self, file_name, locations):
        self.nodes = Strategy(Master_to_slave_replica, self).getNodesWithFile(file_name)
        for node in self.nodes:
            print("retriving file: {}".format(file_name))
            response = node.read(file_name)
            # Will keep trying while there are locations to try on
            if response:
                return response
        return False


    def get_time(self):
        # TODO
        pass
