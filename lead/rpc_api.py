import os
import json
import errno
import threading

from node import Node

from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from jsonrpc import JSONRPCResponseManager, dispatcher
from subprocess import call
from tinydb import TinyDB, Query

'''
This class opens a connection for nodes to register on using RPC
'''

controller = None
ip = None
port = None
db = None
query = None

class RPC(threading.Thread):

    def __init__(self, this_controller, this_ip, this_port):
        threading.Thread.__init__(self)
        global controller, ip, port, db
        controller = this_controller
        ip = this_ip
        port = this_port
        db = TinyDB("nodes.json")
        db.purge_tables()

    @dispatcher.add_method
    def register_node(**kwargs):
        ip = kwargs["ip"]
        mac = kwargs["mac"]
        port = kwargs["port"]
        units = kwargs["units"]
        print("[!] New connection established with Node of MAC={} and IP={}".format(mac, ip))
        if(kwargs["version"] > controller._version):
            print('Updating node code')
            call([os.getcwd() + '/deploy.sh', ip])
            return { "code": 200, "msg": "Updating slave..." }
        else:
            if(db.search(Query().mac == mac)):
                print('Updating node in db')
                db.update({'mac': mac, 'ip': ip, 'port': port, 'units': units}, Query().mac == mac)
            else:
                print('Adding node to db')
                db.insert({'mac': mac, 'ip': ip, 'port': port, 'units': units})
            print("Node registered successfully")
            return { "code": 200, "msg": "Success." }

    @dispatcher.add_method
    def register_location(**kwargs):
        print('Register Location')
        file_name = kwargs["file_name"]
        location = kwargs["location"]  # Node mac
        print("[*] Adding {} to registry for file '{}'".format(location,
                                                               file_name))
        controller.add_to_ledger(file_name, location)

    @Request.application
    def application(self, request):
        response = JSONRPCResponseManager.handle(request.data, dispatcher)
        return Response(response.json, mimetype='application/json')


    def run(self):
        run_simple(ip, port, self.application)
