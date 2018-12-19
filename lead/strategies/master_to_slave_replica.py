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
import time

class Master_to_slave_replica(Strategy):

    def __init__(self, this_controller, desc, nb_replicas):
        Strategy.__init__(self, this_controller, desc)
        self.description = desc
        self.nb_replicas = int(nb_replicas)
        self.controller = this_controller
        self.nodes = []


    def store_file(self, file_bytes, file_name):
        f = open("log.txt", "a+")
        f.write("{}; Enter Strategy: Master_to_slave_replica with {} Replication and {} nodes\n".format(int(round(time.time() * 1000)),self.nb_replicas,len(self.nodes)))
        f.write("{}; Master_to_slave_replica: Find and Shuffle nodes\n".format(int(round(time.time() * 1000))))
        self.nodes = Strategy(Master_to_slave_replica,self).getNodes()
        shuffle(self.nodes)
        f.write("{}; Master_to_slave_replica: nodes shuffled\n".format(int(round(time.time() * 1000))))
        if not self.nodes:
            f.write("{}; Master_to_slave_replica: No Nodes available\n".format(int(round(time.time() * 1000))))
            f.close()
            return False
        i = 0
        for n in range(self.nb_replicas):
            if i > self.nb_replicas or i >= len(self.nodes):
                break;
            f.write("{}; Master_to_slave_replica: Sending file ({}) to {}\n".format(int(round(time.time() * 1000)), file_name, self.nodes[i].mac))
            response = self.nodes[i].write(file_name, file_bytes)
            if response and response["result"]["code"] == 200:
                f.write(
                    "{}; Master_to_slave_replica: File ({}) send to {} success\n".format(int(round(time.time() * 1000)),
                                                                                         file_name, self.nodes[i].mac))
                f.write("{}; Master_to_slave_replica adding file ({}) to ledger on MAC={}\n".format(
                    int(round(time.time() * 1000)), file_name, self.nodes[i].mac))
                self.controller.add_to_ledger(file_name, self.nodes[i].mac, len(file_bytes))
                i = i + 1
            else:
                # If a node can't be written to, it should be considered fatal
                f.close()
                return False
        f.write("{}; Finish Strategy: Master_to_slave_replica with {} Replication and {} nodes\n".format(int(round(time.time() * 1000)),
                                                                                                    self.nb_replicas,
                                                                                                    len(self.nodes)))
        f.close()
        return True


    def retrieve_file(self, file_name, locations):
        self.nodes = Strategy(Master_to_slave_replica, self).getNodesWithFile(file_name)
        f = open("log.txt", "a+")
        for node in self.nodes:
            print("retriving file: {}".format(file_name))
            f.write("{}; Master_to_slave_replica Requesting file ({})\n".format(int(round(time.time() * 1000)),file_name))
            response = node.read(file_name)
            f.write("{}; Master_to_slave_replica file ({}) Rechived\n".format(int(round(time.time() * 1000)), file_name))

            # Will keep trying while there are locations to try on
            if response:
                f.close()
                return response
        f.close()
        return False


    def get_time(self):
        # TODO
        pass
