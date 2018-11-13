#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 theomorales <theomorales@Theos-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.

"""
Node class for the LeadNode project
"""
import requests
import json

class Node:

    def __init__(self, id, mac, ip):
        self.id = id
        self.mac = mac
        self.ip = ip
        self.storage_units = 1
        self.port = 5002

    def set_storage_units(self, nb_units):
        self.storage_units = nb_units

    def write(self, filename, bytes):
        payload = make_payload("write_file", {"filename": filename, "bytes": bytes})
        response = remote_call(payload)

    def read(self, fileName):
        payload = make_payload("read_file",{"filename":fileName})
        response = remote_call(payload)

    def delete(self, fileName):
        payload = make_payload("delete_file",{"filename":fileName})
        response = remote_call(payload)

    def __make_payload(method,params):
        return {
            "method":method,
            "params":params,
            "jsonrpc":"2.0",
            "id":0,
        }
    def __remote_call(payload):
        url = "http://"+self.ip+":"+self.port
        headers = {'content-type':'application/json'}
        return requests.post(url, data = json.dumps(payload), headers=headers).json()
