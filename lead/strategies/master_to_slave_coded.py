#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#
# Distributed under terms of the MIT license.

"""
Master to slave with coding
"""

import kodo

from . import Strategy
from random import shuffle


class Master_to_slave_coded(Strategy):
    def __init__(self, this_controller, desc, losses):
        Strategy.__init__(self, this_controller, desc)
        self.description = desc
        self.losses = losses
        self.controller = this_controller
        self.nodes = []

    def store_file(self, file_bytes, file_name):
        self.nodes = Strategy(Master_to_slave_coded,self).getNodes()
        shuffle(self.nodes)
        print("number of nodes: {}".format(len(self.nodes)))
        if not self.nodes:
            return False
        i = 0
        kodopack_index = 0
        kodo_packages = self.encypt_with_kodo(file_bytes.encode('hex'))
        for package in kodo_packages:
            if i >= len(self.nodes):
                i = 0
            print(file_name)
            response = self.nodes[i].write("{}.kodo.{}".format(file_name,kodopack_index), package)
            if response and response["result"]["code"] == 200:
                print("file uploaded to {}".format(self.nodes[i].mac))
                self.controller.add_to_ledger(file_name, self.nodes[i].mac)
                i = i + 1
                kodopack_index = kodopack_index + 1
            else:
                # If a node can't be written to, it should be considered fatal
                return False
        return True


    def retrieve_file(self, file_name, locations):
        self.nodes = Strategy(Master_to_slave_coded, self).getNodesWithFile(file_name)
        packs = []
        for node in self.nodes:
            print("retriving files: {}".format(file_name))
            response = node.read("{}.kodo".format(file_name))
            packs.extend(response["result"])
            response = self.decypt_with_kodo(packs)
            if response is None:
                continue
            # Will keep trying while there are locations to try on
            if response:
                return response
        return False


    def encypt_with_kodo(self, file_bytes):
        return [file_bytes,file_bytes,file_bytes,file_bytes,file_bytes]

    def decypt_with_kodo(self, file_bytes):
        print(file_bytes[0])
        return {"result":file_bytes[0]}
        #return NONE if it can't be decoded with the amount of packets

    def get_time(self):
        pass
