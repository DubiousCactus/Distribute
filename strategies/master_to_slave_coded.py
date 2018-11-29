#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 theomorales <theomorales@Theos-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.

"""
Master to slave with coding
"""

from . import Strategy
from lead_node import lead
from random import shuffle

class Master_to_slave_coded(Strategy):
    def __init__(self, controller, desc, losses):
        Strategy.__init__(self, controller, desc)
        self.losses = losses

    def store_file(self, file_bytes, file_name):
        nodes = shuffle(self.controller.nodes)
        for node in self.controller.nodes:
            response = node.read_file(file_name)
            if response:
               return response
        return

    def retrieve_file(self, file_name, locations):
        for node in locations:
            response = node.read_file(file_name)
            if response:
               return response
        return

    def encypt_with_kodo(self, file_bytes):
        pass

    def decypt_with_kodo(self, file_bytes):
        pass

    def get_time(self):
        pass
