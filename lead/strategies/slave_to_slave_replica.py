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
import time


class Slave_to_slave_replica(Strategy):

    def __init__(self, this_controller, desc, nb_replicas):
        Strategy.__init__(self, this_controller, desc)
        print("in init")
        self.nb_replicas = int(nb_replicas)
        self.controller = this_controller
        self.nodes = []


    def store_file(self, file_bytes, file_name):
        f = open("log.txt", "a+")
        f.write("{}; Enter Strategy: Slave_to_slave_replica with {} Replication and {} nodes\n".format(int(round(time.time() * 1000)),self.nb_replicas,len(self.nodes)))
        f.write("{}; Slave_to_slave_replica: Find and Shuffle nodes\n".format(int(round(time.time() * 1000))))
        self.nodes = Strategy(Slave_to_slave_replica,self).getNodes()
        self.nodes = shuffle(self.nodes)
        f.write("{}; Slave_to_slave_replica: nodes shuffled\n".format(int(round(time.time() * 1000))))
        if not self.nodes:
            f.write("{}; Slave_to_slave_replica: No Nodes available\n".format(int(round(time.time() * 1000))))
            f.close()
            return False
        i = 0
        for n in range(self.nb_replicas):
            if i > self.nb_replicas or i >= len(self.nodes):
                break;
            f.write("{}; Slave_to_slave_replica: Sending file ({}) to {}\n".format(int(round(time.time() * 1000)),file_name,self.nodes[i].mac))
            response = self.nodes[i].write_repeat(file_name,file_bytes, self.nb_replicas, self.nodes)
            f.write("{}; Slave_to_slave_replica: File ({}) send to {} success\n".format(int(round(time.time() * 1000)),file_name,self.nodes[i].mac))
            f.write("{}; Finish Strategy: Slave_to_slave_replica with {} Replication and {} nodes\n".format(int(round(time.time() * 1000)),self.nb_replicas,len(self.nodes)))
            f.close()
            return response
        f.close()
        return True


    def retrieve_file(self, file_name, locations):
        self.nodes = Strategy(Slave_to_slave_replica, self).getNodesWithFile(file_name)
        f = open("log.txt", "a+")
        for node in self.nodes:
            print("retriving file: {}".format(file_name))
            f.write("{}; Slave_to_slave_replica Requesting file ({})\n".format(int(round(time.time() * 1000)), file_name))
            response = node.read(file_name)
            f.write("{}; Slave_to_slave_replica file ({}) Rechived\n".format(int(round(time.time() * 1000)),file_name))
            # Will keep trying while there are locations to try on
            if response:
                f.close()
                return response
        f.close()
        return False

    def get_time(self):
        pass


