#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#
# Distributed under terms of the MIT license.

"""
Slave to slave with coding
"""

from . import Strategy
from random import shuffle
import time

class Slave_to_slave_coded(Strategy):
    def __init__(self, this_controller, desc, losses):
        Strategy.__init__(self, this_controller, desc)
        self.description = desc
        self.losses = losses
        self.controller = this_controller
        self.nodes = []

    def store_file(self, file_bytes, file_name):
        f = open("log.txt", "a+")
        f.write("{}; Enter Strategy: Slave_to_slave_coded with {} Replication and {} nodes\n".format(
            int(round(time.time() * 1000)), self.losses, len(self.nodes)))
        f.write("{}; Slave_to_slave_coded: Find and Shuffle nodes\n".format(int(round(time.time() * 1000))))

        self.nodes = Strategy(Slave_to_slave_coded, self).getNodes()
        self.nodes = shuffle(self.nodes)
        f.write("{}; Slave_to_slave_coded: nodes shuffled\n".format(int(round(time.time() * 1000))))
        if not self.nodes:
            f.write("{}; Slave_to_slave_coded: No Nodes available\n".format(int(round(time.time() * 1000))))
            f.close()
            return False
        for node in self.nodes:
            f.write("{}; Slave_to_slave_coded: Sending file ({}) to {}\n".format(int(round(time.time() * 1000)),file_name,node.mac))
            response = node.write_kodo_repeat(file_name, file_bytes, self.losses, self.nodes)
            f.write("{}; Slave_to_slave_coded: File ({}) send to {} success\n".format(int(round(time.time() * 1000)),
                                                                                        file_name, node.mac))
            f.write("{}; Finish Strategy: Slave_to_slave_coded with {} Replication and {} nodes\n".format(
                int(round(time.time() * 1000)), self.losses, len(self.nodes)))
            f.close()
            return response
        f.close()
        return False

    def retrieve_file(self, file_name, locations):
        self.nodes = Strategy(Slave_to_slave_coded, self).getNodesWithFile(file_name)
        for node in self.nodes:
            print("retriving file: {}".format(file_name))
            response = node.read_kodo_files(file_name,self.nodes)
            # Will keep trying while there are locations to try on
            if response:
                return response
        return False

    def get_time(self):
        pass
