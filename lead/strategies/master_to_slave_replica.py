#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 theomorales <theomorales@Theos-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.

"""
Master to slave using replication
"""

from . import Strategy
from random import shuffle

class Master_to_slave_replica(Strategy):
    def __init__(self, controller, desc, nb_replicas, losses):
        Strategy.__init__(self, controller, desc)
        self.nb_replicas = nb_replicas
        self.losses = losses


    def store_file(self, file_bytes, file_name):
        nodes = shuffle(self.controller.nodes)
        if not nodes: return False
        for n in range(self.nb_replicas):
            for node in nodes:
                response = node.write(file_name)
                if response and response['code'] == 200:
                    self.controller.add_to_ledger(file_name, node)
                    nodes.remove(node) # No more than once per node
                else:
                    # If a node can't be written to, it should be considered fatal
                    return False
        return True


    def retrieve_file(self, file_name, locations):
        for node in locations:
            response = node.read_file(file_name)
            # Will keep trying while there are locations to try on
            if response and response['code'] == 200:
                return response
        return False


    def get_time(self):
        # TODO
        pass
