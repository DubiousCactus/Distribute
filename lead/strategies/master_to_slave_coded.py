#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#
# Distributed under terms of the MIT license.

"""
Master to slave with coding
"""

from . import Strategy
from random import shuffle
import time
from master_kodo import MasterKodo

class Master_to_slave_coded(Strategy):
    def __init__(self, this_controller, desc, losses):
        Strategy.__init__(self, this_controller, desc)
        self.description = desc
        self.losses = losses
        self.controller = this_controller
        self.nodes = []
        self.kodoencoder = MasterKodo()
        self.replicas = 4

    def store_file(self, file_bytes, file_name):
        f = open("log.txt", "a+")
        f.write("{}; Enter Strategy: Master_to_slave_coded with {} Loses and {} nodes\n".format(int(round(time.time() * 1000)),self.losses,len(self.nodes)))
        f.write("{}; Master_to_slave_coded: Find and Shuffle nodes\n".format(int(round(time.time() * 1000))))
        self.nodes = Strategy(Master_to_slave_coded,self).getNodes()
        self.nodes = shuffle(self.nodes)
        f.write("{}; Master_to_slave_coded: nodes shuffled\n".format(int(round(time.time() * 1000))))
        if not self.nodes:
            f.write("{}; Master_to_slave_coded: No Nodes available\n".format(int(round(time.time() * 1000))))
            return False
        i = 0
        kodopack_index = 0
        f.write("{}; Master_to_slave_coded: Enter encoding\n".format(int(round(time.time() * 1000))))
        f.close()
        kodo_packages = self.encypt_with_kodo(file_bytes,self.losses)
        f = open("log.txt", "a+")
        for package in kodo_packages:
            if i >= len(self.nodes):
                i = 0
            f.write("{}; Master_to_slave_coded: Sending file ({}) to {}\n".format(int(round(time.time() * 1000)), file_name, self.nodes[i].mac))
            response = self.nodes[i].write("{}.kodo.{}".format(file_name,kodopack_index), str(package))
            if response and response["result"]["code"] == 200:
                f.write(
                    "{}; Master_to_slave_coded: File ({}) send to {} success\n".format(int(round(time.time() * 1000)),
                                                                                         file_name, self.nodes[i].mac))
                f.write("{}; Master_to_slave_coded adding file ({}) to ledger on MAC={}\n".format(
                    int(round(time.time() * 1000)), file_name, self.nodes[i].mac))
                print(len(file_bytes))
                self.controller.add_to_ledger(file_name, self.nodes[i].mac, len(file_bytes))
                i = i + 1
                kodopack_index = kodopack_index + 1
            else:
                # If a node can't be written to, it should be considered fatal
                return False
        f.write("{}; Finish Strategy: Master_to_slave_coded with {} Loses and {} nodes\n".format(int(round(time.time() * 1000)),
                                                                                                    self.losses,
                                                                                                    len(self.nodes)))
        f.close()
        return True


    def retrieve_file(self, file_name, locations):
        self.nodes = Strategy(Master_to_slave_coded, self).getNodesWithFile(file_name)
        f = open("log.txt", "a+")
        packs = []
        for node in self.nodes:
            print("retriving files: {}".format(file_name))
            response = node.read("{}.kodo.".format(file_name))
            packs.extend(response["result"])
            f.write("{}; Master_to_slave_coded receive file ({}) as kodo from node with MAC={}\n".format(
                int(round(time.time() * 1000)), file_name, node.mac))
            response = self.decypt_with_kodo(file_name,packs)
            if response is None:
                f.write("{}; Master_to_slave_coded could not decode with the amount of data given\n".format(
                    int(round(time.time() * 1000))))
                continue
            # Will keep trying while there are locations to try on
            if response:
                f.write("{}; Master_to_slave_coded Finished decoding file ({}) from node with MAC={}\n".format(
                    int(round(time.time() * 1000)), file_name, node.mac))
                f.close()
                return {"result":str(response).encode('hex')}
        f.close()
        return False

    def encypt_with_kodo(self, file_bytes,loses):
        data = bytearray(file_bytes)
        symbol_size = len(data)/self.replicas
        symbols = len(data) / symbol_size
        f = open("log.txt", "a+")
        self.kodoencoder.init_encoder(symbols, symbol_size)
        f.write("{}; Master_to_slave_coded Encoding starts with data length:{}, symbol_size: {}, symbols: {} \n".format(
            int(round(time.time() * 1000)), len(data), symbol_size, symbols))
        [data_in, encoded_packets] = self.kodoencoder.encode(data, symbols, loses)
        f.write("{}; Master_to_slave_coded Encoded {} packages successfully\n".format(int(round(time.time() * 1000)),len(encoded_packets)))
        f.close()
        return encoded_packets

    def decypt_with_kodo(self ,file_name, file_bytes):
        filesize = Strategy(Master_to_slave_coded, self).getFileSize(file_name)
        print("original filesize: {} for file: {}".format(filesize,file_name))
        symbol_size = filesize/self.replicas
        symbols = filesize / symbol_size
        self.kodoencoder.init_decoder(symbols, symbol_size)
        f = open("log.txt", "a+")
        f.write("{}; Master_to_slave_coded Decoding {} packages\n".format(int(round(time.time() * 1000)),len(file_bytes)))
        data_out = self.kodoencoder.decode(file_bytes)
        return data_out

    def get_time(self):
        pass
