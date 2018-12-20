import sys
import json
import netifaces as ni

from node import Node
from lead import LeadNode
from rpc_server import Server
import time
from uuid import getnode as get_mac


class ClientNode:

    def __init__(self, config, debug=False):
        self.debug = debug
        if debug:
            config['lead_ip'] = 'localhost'

        self.leadNode = LeadNode(config['lead_ip'], config['lead_port'])
        self.port = config['port']
        self._version = config['version']
        self.storage_units = config['storage_units']
        self.neighbours = {}
        self.server = Server(self, hex(get_mac()), self.get_ip(), self.port)


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
            self.register_location(name)
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
        if self.debug:
            return "localhost"
        else:
            return ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']


    def register(self):
        try:
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
        except:
            time.sleep(20)
            self.register()


    def register_location(self, file_name):
        respone = self.leadNode.call(
            self.make_payload(
                "register_location",
                {
                    "file_name": file_name,
                    "location": hex(get_mac()),
                }
            )
        )


if __name__ == "__main__":
    debug = (len(sys.argv) > 1 and sys.argv[1] == '--debug')
    with open('config.json') as config_file:
        client = ClientNode(json.load(config_file), debug)
        client.start()
