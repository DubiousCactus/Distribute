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

class Slave_to_slave_coded(Strategy):
    def __init__(self, this_controller, desc, losses):
        Strategy.__init__(self, this_controller, desc)
        self.description = desc
        self.losses = losses
        self.controller = this_controller
        self.nodes = []

    def store_file(self, file_bytes, file_name):
        self.nodes = Strategy(Slave_to_slave_coded, self).getNodes()
        print("From strategy:")
        shuffle(self.nodes)
        print("number of nodes: {}".format(len(self.nodes)))
        if not self.nodes:
            return False
        for node in self.nodes:
            response = node.write_kodo_repeat(file_name, file_bytes, self.losses, self.nodes)
            return response
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
