#! /usr/bin/pyrhon3

import os
import errno
from node import Node

from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from jsonrpc import JSONRPCResponseManager, dispatcher


class LeadNode:
    def __init__(self, port):
        self.addr = 'localhost'
        self.port = port
        self.nodes = []


    #CREATE FILE
    @dispatcher.add_method
    def registerNode(self, **kwargs):
        print('New connection established with ' + kwargs["ip"])
        self.nodes[kwargs["mac"]]
            = Node(self.lastId + 1, kwargs["mac"], kwargs["ip"])

        return { "code": 200, "msg": "Success." }


    #APPLICATION
    @Request.application
    def application(self, request):
        response = JSONRPCResponseManager.handle(request.data, dispatcher)
        return Response(response.json, mimetype='application/json')


    def start(self):
        run_simple(self.addr, self.port, self.application)


if __name__ == '__main__':
    leadNode = LeadNode(5001)
    leadode.start()
