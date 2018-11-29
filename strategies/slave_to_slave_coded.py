#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 theomorales <theomorales@Theos-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.

"""
Slave to slave with coding
"""

from . import Strategy
from lead_node import lead
from random import shuffle


class Slave_to_slave_coded(Strategy):
    def __init__(self, controller, desc, losses):
        Strategy.__init__(self, controller, desc)
        self.losses = losses

    def store_file(self, file_bytes, file_name):
        node = random.choice(self.controller.nodes)
        replications = self.description["nb_replicas"]
        encrypted_data = encypt_with_kodo()
        return node.write_file_repeat(file_name, encrypted_data, replications)

    def retrieve_file(self, file_name, locations):
        for node in locations:
            response = node.read_file(file_name)
            if response:
               return decypt_with_kodo(response)
        return

    def encypt_with_kodo(self, file_bytes):
        pass

    def decypt_with_kodo(self, file_bytes):
        pass

    def get_time(self):
        pass
