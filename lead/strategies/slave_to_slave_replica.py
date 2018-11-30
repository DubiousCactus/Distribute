#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 theomorales <theomorales@Theos-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.

"""
Slave to slave with replication
"""

from . import Strategy
from random import shuffle

class Slave_to_slave_replica(Strategy):
    def __init__(self, controller, desc, nb_replicas, losses):
        Strategy.__init__(self, controller, desc)
        self.nb_replicas = nb_replicas
        self.losses = losses

    def store_file(self, file_bytes, file_name):
        node = random.choice(self.controller.nodes)
        replications = self.description["nb_replicas"]
        return node.write_file_repeat(file_name, replications)

    def retrieve_file(self, file_name, locations):
        for node in locations:
            response = node.read_file(file_name)
            if response:
               return response
        return

    def get_time(self):
        pass


