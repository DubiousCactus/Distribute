#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 theomorales <theomorales@Theos-MacBook-Pro.local>
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
        payload = make_payload("write_file", {"file_name": filename, "bytes": bytes})
        return self.__remote_call(payload)


    def write_repeat(self, filename, bytes, iterations):
        payload = make_payload(
            "write_file_repeat",
            {"file_name": filename, "bytes": bytes, "ttl":iterations}
        )
        return self.__remote_call(payload)


    def read(self, fileName):
        payload = make_payload("read_file", {"file_name": fileName})
        return self.__remote_call(payload)


    def delete(self, fileName):
        payload = make_payload("delete_file", {"file_name": fileName})
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


    def __make_payload(method,params):
        return {
            "method": method,
            "params": params,
            "jsonrpc": "2.0",
            "id": 0,
        }


    def __remote_call(payload):
        url = "http://{}:{}".format(self.ip, self.port)
        headers = {'content-type': 'application/json'}
        return requests.post(url, data=json.dumps(payload), headers=headers).json()
