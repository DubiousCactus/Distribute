import os
import json
import errno

from node import Node
from werkzeug import secure_filename
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response

#This class opens a connection for nodes to register on using RPC
class RpcApi:
    
    def __init__(self, nodes, ip, port, version):
        self.ip = ip
        self.port = port
        self.version = version
        self.nodes = nodes
        self.lastId = 0
    
    def getCodeVersion(self):
        return self.version

    def updateCodeOnSlave(self, ip):
        # TODO: Maybe sanitize the ip first ?
        call(['deploy.sh', ip])

    @dispatcher.add_method
    def registerNode(self, **kwargs):
        clientIp = kwargs["ip"]
        clientMac = kwargs["mac"]
        print('New connection established with ' + clientIp)
        #The Node Requesting for registration, has a invalid version of the code, an update will be forced on to it.
        if(kwargs["code"] > getCodeVersion()):
            updateCodeOnSlave(clientIp)
            return { "code": 200, "msg": "Updating slave..." }
        #The Node Requesting for registration, has the newest version of API and can therefore be added to the directory
        else:
            self.nodes[clientMac] = Node(self.lastId, clientMac, clientIp)
            self.lastId += 1
            return { "code": 200, "msg": "Success." }

    @Request.application
    def application(self, request):
        response = JSONRPCResponseManager.handle(request.data, dispatcher)
        return Response(response.json, mimetype='application/json')

    def start(self):
        run_simple(self.ip, self.port, self.application)