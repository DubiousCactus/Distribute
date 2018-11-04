#! /usr/bin/python3

import os
import errno
from node import Node

from werkzeug import secure_filename
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from flask import Flask, render_template, request
from jsonrpc import JSONRPCResponseManager, dispatcher

app = Flask(__name__)

class LeadNode:
    def __init__(self, addr, api_port, rpc_port):
        self.addr = addr
        self.api_port = api_port
        self.rpc_port = rpc_port
        self.nodes = []


    @app.route('/')
    def showpage():
       return render_template('upload.html')

    @app.route('/storage', methods = ['GET','POST'])
    def upload_file():

       if request.method == 'POST':
          f = request.files['file']
          f.save(secure_filename(f.filename)) #WILL BE REMOVED BECAUSE WE DONT STORE ON THE PI3
          #REMOTE CALL TO RANDOM NODE IN THE SYSTEM USING RPC
          return 'file uploaded successfully'

       if request.method == 'GET':
             return 'returned '+ request.args["filename"]+' successfully'
             #return 'returning '+ fileEntered +' successfully'


    @dispatcher.add_method
    def registerNode(self, **kwargs):
        print('New connection established with ' + kwargs["ip"])
        self.nodes[kwargs["mac"]] = Node(self.lastId + 1, kwargs["mac"], kwargs["ip"])

        return { "code": 200, "msg": "Success." }


    #APPLICATION
    @Request.application
    def application(self, request):
        response = JSONRPCResponseManager.handle(request.data, dispatcher)
        return Response(response.json, mimetype='application/json')


    def start(self):
        app.run(debug=True, host=self.addr, port=self.api_port)
        run_simple(self.addr, self.rpc_port, self.application)


if __name__ == '__main__':
    leadNode = LeadNode("172.24.1.1", 5000, 5001)
    leadNode.start()
