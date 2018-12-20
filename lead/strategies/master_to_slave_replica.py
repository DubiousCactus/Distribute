#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#
# Distributed under terms of the MIT license.

"""
Master to slave using replication
"""

from . import Strategy
from random import shuffle
import time

class Master_to_slave_replica(Strategy):
    def __init__(self, controller, desc, nb_replicas, losses):
        Strategy.__init__(self, controller, desc)
        self.__controller = controller
        self.nb_replicas = nb_replicas
        self.losses = losses


    def store_file(self, file_bytes, file_name):
        f = open("log.txt", "a+")
        f.write("{}; Enter Strategy: Master_to_slave_replica with {} Replication and {} nodes\n".format(int(round(time.time() * 1000)),self.nb_replicas,len(self.nodes)))
        f.write("{}; Master_to_slave_replica: Find and Shuffle nodes\n".format(int(round(time.time() * 1000))))
        f.write("{}; Master_to_slave_replica: nodes shuffled\n".format(int(round(time.time() * 1000))))
        print("From strategy:")
        print(self.__controller.nodes)
        nodes = shuffle(self.__controller.nodes)
        print("Shuffled nodes:")
        print(nodes)
        if not self.nodes:
            f.write("{}; Master_to_slave_replica: No Nodes available\n".format(int(round(time.time() * 1000))))
            f.close()
            return False
        for n in range(self.nb_replicas):
            for node in nodes:
                print("Attempting to write to node {} ...".format(node.ip))
                f.write("{}; Master_to_slave_replica: Sending file ({}) to {}\n".format(int(round(time.time() * 1000)), file_name, self.nodes[i].mac))
                response = node.write(file_name, file_bytes)
                print("Response: {}".format(reponse))
                if response and response['result']['code'] == 200:
                    f.write(
                            "{}; Master_to_slave_replica: File ({}) send to {} success\n".format(int(round(time.time() * 1000)),
                                                                                                 file_name, self.nodes[i].mac))
                    f.write("{}; Master_to_slave_replica adding file ({}) to ledger on MAC={}\n".format(
                                                                                                    int(round(time.time() * 1000)), file_name, self.nodes[i].mac))
                    # self.__controller.add_to_ledger(file_name, node)
                    nodes.remove(node) # No more than once per node
                else:
                    # If a node can't be written to, it should be considered fatal
                    f.close()
                    return False
            f.write("{}; Finish Strategy: Master_to_slave_replica with {} Replication and {} nodes\n".format(int(round(time.time() * 1000)),
                                                                                                                     self.nb_replicas,
                                                                                                                     len(self.nodes)))
            f.close()
            return True


    def retrieve_file(self, file_name, locations):
        f = open("log.txt", "a+")
        for node in locations:
            print("retriving file: {}".format(file_name))
            f.write("{}; Master_to_slave_replica Requesting file ({})\n".format(int(round(time.time() * 1000)),file_name))
            response = node.read(file_name)
            f.write("{}; Master_to_slave_replica file ({}) Rechived\n".format(int(round(time.time() * 1000)), file_name))

            # Will keep trying while there are locations to try on
            if response:
                f.close()
                return response
        f.close()
        return False


    def get_time(self):
        # TODO
        pass
