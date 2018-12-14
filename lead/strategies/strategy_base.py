#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 theomorales <theomorales@Theos-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.

"""
Strategy base class
"""

from abc import ABCMeta, abstractmethod
from tinydb import TinyDB
from node import Node


class Strategy(object):
    def __init__(self, this_controller, this_description=None):
        self.description = this_description
        self.controller = this_controller
        self.db = TinyDB("nodes.json")
        self.nodes = []

    @abstractmethod
    def store_file(self, file_bytes, file_name):
        pass

    @abstractmethod
    def retrieve_file(self, file_name, locations):
        pass

    @abstractmethod
    def get_time(self):
        pass

    def getNodes(self):
        for item in self.db:
            node = Node(item['mac'],item['ip'],item['port'],item['units'])
            self.nodes.append(node)
        return self.nodes