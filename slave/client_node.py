#! /usr/bin/python3

import json
import requests
import netifaces as ni

from uuid import getnode as get_mac
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from jsonrpc import JSONRPCResponseManager, dispatcher

class ClientNode:

    def __init__(self, config):
        self.leadIP = config['lead_ip']
        self.leadPort = config['lead_port']
        self.port = config['port']
        self._version = config['version']
        self.register()

    def start(self):
        # Starts the communication service as a server
        run_simple(get_ip(), self.leadPort, application)

    def read_file(self, filepath):
        file = open(filepath, "rb").read()
        return file

    def make_payload(self, method, params):
        return {
            "method": method,
            "params": params,
            "jsonrpc": "2.0",
            "id": 0,
        }

    def get_ip(self):
        return ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']

    def remote_call(self, payload):
        url = "http://{}:{}".format(self.leadIP, self.leadReqestPort)
        headers = {'content-type': 'application/json'}
        return requests.post(url, data=json.dumps(payload), headers=headers).json()

    def register(self):
        payload = self.make_payload(
            "registerNode",
            {
                "ip": self.get_ip(),
                "mac": hex(self.get_mac()),
                "code": self._version
            }
        )
        response = remote_call(payload)

    #SERVER PART START
    @dispatcher.add_method
    def write_file(**kwargs):
        TO = os.getcwd()+"\\"+kwargs["filename"]
        file = open(TO, "ab")
        file.write(kwargs["bytes"])
        file.close()
        # IF TRUE AND X > 0 ASK FOR RANDOM NODE REPLICACE TO THAT
        # ELSE RETURN
        return "success"

    @dispatcher.add_method
    def read_file(**kwargs):
        return read_file(kwargs["filename"])

    @dispatcher.add_method
    def delete_file(**kwargs):
        os.remove(kwargs["filename"])
        return "success"

    @Request.application
    def application(request):
        response = JSONRPCResponseManager.handle(request.data, dispatcher)
        print(request.data)
        return Response(response.json,mimetype='application/json')
    #SERVER PART END


if __name__ == "__main__":
    with open('config.json') as config_file:
        client = ClientNode(json.load(config_file))
        client.start()
