import os
import json
import errno

from node import Node

from werkzeug import secure_filename
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from jsonrpc import JSONRPCResponseManager, dispatcher

'''
This class opens a connection for nodes to register on using RPC
'''

class RPC:

    def __init__(self, controller, ip, port):
        self.controller = controller
        self.ip = ip
        self.port = port


    @dispatcher.add_method
    def register_node(self, **kwargs):
        print('[!] New connection established with ' + ip)

        ip = kwargs["ip"]
        mac = kwargs["mac"]
        port = kwwargs["port"]
        units = kwargs["units"]

        if(kwargs["version"] > self.controller._version):
            self.controller.update_node(ip)
            return { "code": 200, "msg": "Updating slave..." }
        else:
            self.controller.add_node(ip, mac, port, units)
            return { "code": 200, "msg": "Success." }


    @Request.application
    def application(self, request):
        response = JSONRPCResponseManager.handle(request.data, dispatcher)
        return Response(response.json, mimetype='application/json')


    def start(self):
        run_simple(self.ip, self.port, self.application)
