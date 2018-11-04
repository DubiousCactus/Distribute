#! /usr/bin/pyrhon3

import os
import errno
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from jsonrpc import JSONRPCResponseManager, dispatcher

Nodes = []

#CREATE FILE
@dispatcher.add_method
def registerNode(**kwargs):
    print('New connection established with ' + kwargs["ip"])
    Nodes.append(kwargs["ip"])
    print('The new connection is stored as Node number ' + str(len(Nodes))+ ' with the IP of ' + Nodes[len(Nodes)-1])
    return "success"

#APPLICATION
@Request.application
def application(request):
    response = JSONRPCResponseManager.handle(request.data, dispatcher)
    #print(request.data)
    return Response(response.json,mimetype='application/json')

if __name__ == '__main__':
    run_simple('localhost',5001,application)
