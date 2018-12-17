#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#
# Distributed under terms of the MIT license.

"""
Slave to slave with replication
"""

from . import Strategy
from random import shuffle


class Slave_to_slave_replica(Strategy):
    def __init__(self, this_controller, desc, nb_replicas):
        Strategy.__init__(self, this_controller, desc)
        print("in init")
        self.nb_replicas = nb_replicas
        self.controller = this_controller
        self.nodes = []


    def store_file(self, file_bytes, file_name):
        self.nodes = Strategy(Slave_to_slave_replica,self).getNodes()
        print("From strategy:")
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
            response = self.nodes[i].write_repeat(file_name,file_bytes, self.nb_replicas, self.nodes)
            return response
        return True


    def retrieve_file(self, file_name, locations):
        self.nodes = Strategy(Slave_to_slave_replica, self).getNodesWithFile(file_name)
        for node in self.nodes:
            print("retriving file: {}".format(file_name))
            response = node.read(file_name)
            # Will keep trying while there are locations to try on
            if response:
                return response
        return False

    def get_time(self):
        pass


