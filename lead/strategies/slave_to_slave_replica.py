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


    # TODO: Make sure the TTL is properly decremented
    def store_file(self, file_bytes, file_name):
        node = random.choice(self.controller.nodes)
        return node.write_file_repeat(file_name, self.nb_replicas)


    def retrieve_file(self, file_name, locations):
        for node in locations:
            response = node.read_file(file_name)
            # Will keep trying while there are locations to try on
            if response and response['code'] == 200:
                return response
        return


    def get_time(self):
        pass


