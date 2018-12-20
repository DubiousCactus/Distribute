#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#
# Distributed under terms of the MIT license.

"""
Node class for the LeadNode project. Defines a Node/Slave as a object, and is enable to call the Node/Slave remote functions
"""

import requests
import json


class Node:

    def __init__(self, mac, ip, port=5000, units=1):
        self.mac = mac
        self.ip = ip
        self.storage_units = units
        self.port = port


    def set_storage_units(self, nb_units):
        self.storage_units = nb_units


    def write(self, filename, bytes):
        payload = self.make_payload("write_file", {"file_name": filename, "bytes": bytes})
        return self.__remote_call(payload)


    def write_repeat(self, filename, bytes, iterations, nodes):
        payload = self.__make_payload(
            "write_file_repeat",
            {"name": filename, "content": bytes.encode('hex'), "nodes":nodes, "ttl":iterations}
        )
        return self.__remote_call(payload)


    def jsonify_kodo_packets(self, packs):
        jsonnodes = None
        for pack in packs:
            if jsonnodes is not None:
                jsonnodes = jsonnodes + ","
            else:
                jsonnodes = ""
            temp = r'"pack":"{}"'.format(pack)
            jsonnodes = jsonnodes + '{' + temp + '}'
        return "["+jsonnodes+"]"

    def write_kodo_repeat(self, filename, bytes, loses, nodes, coded, index):
        payload = self.__make_payload("write_files_kodo_repeat", {"name": filename, "content": self.jsonify_kodo_packets(bytes), "loses":loses, "nodes":nodes, "coded":coded,"index":index})
        return self.__remote_call(payload)


    def read(self, fileName):
        payload = self.make_payload("read_file", {"file_name": fileName})
        return self.__remote_call(payload)


    def delete(self, fileName):
        payload = self.make_payload("delete_file", {"file_name": fileName})
        return self.__remote_call(payload)


    # Propagate a node registration to the other nodes
    def propagate(self, mac, ip, port, units):
        payload = self.__make_payload(
            "add_neighbour",
            {
                "mac": mac,
                "ip": ip,
                "port": port,
                "units": units
            }
        )
        return self.__remote_call(payload)


    def __make_payload(self,method,params):
        return {
            "method": method,
            "params": params,
            "jsonrpc": "2.0",
            "id": 0,
        }


    def __remote_call(self,payload):
        url = "http://{}:{}".format(self.ip, self.port)
        headers = {'content-type': 'application/json'}
        return requests.post(url, data=json.dumps(payload), headers=headers).json()
