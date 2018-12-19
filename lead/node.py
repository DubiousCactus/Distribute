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
        payload = self.__make_payload("write_file", {"name": filename, "content": bytes.encode('hex')})
        return self.__remote_call(payload)

    def write_kodo_repeat(self, filename, bytes, loses, nodes):
        payload = self.__make_payload("write_files_kodo_repeat", {"name": filename, "content": bytes.encode('hex'), "loses":loses, "nodes":self.jsonityNodes(nodes), "coded":False,"index":0})
        return self.__remote_call(payload)


    def jsonityNodes(self, nodes):
        jsonnodes = None
        for node in nodes:
            if jsonnodes is not None:
                jsonnodes = jsonnodes + ","
            else:
                jsonnodes = ""
            temp = r'"mac":"{}","ip":"{}","port":{},"units":{}'.format(node.mac,node.ip,node.port,node.storage_units)
            jsonnodes = jsonnodes + '{' + temp + '}'
        return "["+jsonnodes+"]"

    def write_repeat(self, filename, bytes, iterations, nodes):
        payload = self.__make_payload(
            "write_file_repeat",
            {"name": filename, "content": bytes.encode('hex'), "nodes":self.jsonityNodes(nodes), "ttl":iterations}
        )
        return self.__remote_call(payload)

#    def write_files_kodo_repeat(self, filename, bytes, kodo_content, iterations, nodes):
#        payload = self.__make_payload(
#            "write_files_kodo_repeat",
#            {"name": filename, "content": bytes.encode('hex'), "nodes":self.jsonityNodes(nodes), "ttl":iterations, "kodo_content":kodo_content}
#        )
#        return self.__remote_call(payload)

    def read(self, fileName):
        payload = self.__make_payload("read_file", {"name": fileName})
        return self.__remote_call(payload)

    def read_kodo(self, fileName, nodes):
        payload = self.__make_payload("read_kodo_files", {"name": fileName, "nodes":self.jsonityNodes(nodes)})
        return self.__remote_call(payload)


    def delete(self, fileName):
        payload = self.__make_payload("delete_file", {"file_name": fileName})
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


    def __make_payload(self, method, params):
        return {
            "method": method,
            "params": params,
            "jsonrpc": "2.0",
            "id": 0,
        }


    def __remote_call(self, payload):
        url = "http://{}:{}".format(self.ip, self.port)
        headers = {'content-type': 'application/json'}
        return requests.post(url, data=json.dumps(payload), headers=headers).json()
