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
          f.save(secure_filename(f.filename))
          # (TESTING REPLICAITON)
          # IF TRUE SEND TO RANDOM NODE 
          # ELSE SEND TO X NODES
          return { "code": 200, "msg": 'File uploaded successfully.' }

       if request.method == 'GET':
           # GET THE FILE FROM A NODE
             return 'returned '+ request.args["filename"]+' successfully'
             #return 'returning '+ fileEntered +' successfully'

    def getCodeVersion():
        pass
    def updateCodeOnSlave(ip):
        #IMPLEMENT THEO CODE TO UPDATE THE CLIENT
        pass
    @dispatcher.add_method
    def registerNode(self, **kwargs):
        print('New connection established with ' + kwargs["ip"])
        #UPDATE THE CODE ON THAT NODE
        if(kwargs["code"] > getCodeVersion()):
            updateCodeOnSlave(kwargs["ip"])
            return { "code": 200, "msg": "Updating slave..." }
        else:
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
