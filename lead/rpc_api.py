import os
import json
import errno

from node import Node
from werkzeug import secure_filename
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response

#This class opens a connection for nodes to register on using RPC
class RpcApi:

    def __init__(self, controller, ip, port):
        self.ip = ip
        self.port = port

    @dispatcher.add_method
    def registerNode(self, **kwargs):
        ip = kwargs["ip"]
        mac = kwargs["mac"]
        print('New connection established with ' + ip)
        #The Node Requesting for registration, has a invalid version of the code, an update will be forced on to it.
        if(kwargs["version"] > self.controller._version):
            self.controller.updateSlave(ip)
            return { "code": 200, "msg": "Updating slave..." }
        #The Node Requesting for registration, has the newest version of API and can therefore be added to the directory
        else:
            self.controller.addNode(ip, mac)
            return { "code": 200, "msg": "Success." }

    @Request.application
    def application(self, request):
        response = JSONRPCResponseManager.handle(request.data, dispatcher)
        return Response(response.json, mimetype='application/json')

    def start(self):
        run_simple(self.ip, self.port, self.application)
