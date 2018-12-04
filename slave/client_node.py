#! /usr/bin/python3

import json
import netifaces as ni

from node import Node
from lead import LeadNode
from rpc_server import Server

from uuid import getnode as get_mac


class ClientNode:

    def __init__(self, config):
        self.leadNode = LeadNode(config['lead_ip'], config['lead_port'])
        self.port = config['port']
        self.server = None
        self._version = config['version']
        self.storage_units = config['storage_units']
        self.neighbours = {}
        self.server = Server(self, self.get_ip(), self.port)


    def start(self):
        self.server.start()
        self.register()


    def add_neighbour(self, mac, ip, port, units):
        self.neighbours[mac] = Node(ip, port, units)


    def read_file(self, filepath):
        with open(filepath, "rb") as file:
            return file.read() # TODO: Serialize before return


    def write_file(self, name, content):
        with open(name, "wb") as file:
            file.write(content)
            return True

        return False


    def pick_and_repeat(self, name, content, ttl):
        for mac, node in self.neighbours:
            # TODO: Criteria
            node.write_repeat(name, content, ttl)
            break # Escape for loop


    def make_payload(self, method, params):
        return {
            "method": method,
            "params": params,
            "jsonrpc": "2.0",
            "id": 0,
        }


    def get_ip(self):
        return ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']


    def register(self):
        payload = self.make_payload(
            "register_node",
            {
                "ip": self.get_ip(),
                "mac": hex(get_mac()),
                "version": self._version,
                "port": self.port,
                "units": self.storage_units
            }
        )
        response = self.leadNode.call(payload)
        # TODO: Check response



if __name__ == "__main__":
    with open('config.json') as config_file:
        client = ClientNode(json.load(config_file))
        client.start()
