#! /usr/bin/python3

import json
import netifaces as ni

from lead import LeadNode
from rpc_server import Server
from uuid import getnode as get_mac

class ClientNode:

    def __init__(self, config):
        self.leadNode = LeadNode(config['lead_ip'], config['lead_port'])
        self.port = config['port']
        self.server = None
        self._version = config['version']

    def start(self):
        self.server = Server(self, self.get_ip(), self.port)
        self.register()

    def read_file(self, filepath):
        with open(filepath, "rb") as file:
            return file.read() # TODO: Serialize before return

    def make_payload(self, method, params):
        return {
            "method": method,
            "params": params,
            "jsonrpc": "2.0",
            "id": 0,
        }

    def get_ip(self):
        # return ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
        return "1"

    def register(self):
        payload = self.make_payload(
            "registerNode",
            {
                "ip": self.get_ip(),
                "mac": hex(get_mac()),
                "code": self._version
            }
        )
        response = self.leadNode.call(payload)
        # TODO: Check response



if __name__ == "__main__":
    with open('config.json') as config_file:
        client = ClientNode(json.load(config_file))
        client.start()
