#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#
# Distributed under terms of the MIT license.

"""
Strategy base class
"""

from abc import ABCMeta, abstractmethod
from tinydb import TinyDB, Query
from node import Node
import json


class Strategy(object):
    def __init__(self, this_controller, this_description=None):
        self.description = this_description
        self.controller = this_controller
        self.ledger = TinyDB("ledger.json")
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
        self.nodes = []
        for item in self.db:
            node = Node(item['mac'],item['ip'],item['port'],item['units'])
            self.nodes.append(node)
        return self.nodes

    def getNodesWithFile(self,filename):
        macs = self.ledger.search(Query().file_name == filename)
        self.nodes = []
        for item in macs:
            mac = item["location"]
            dbnode = self.db.get(Query().mac == mac)
            if(dbnode == None):
                continue
            node = Node(dbnode['mac'],dbnode['ip'],dbnode['port'],dbnode['units'])
            self.nodes.append(node)
        return self.nodes