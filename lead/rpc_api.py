import os
import json
import errno
import threading

from node import Node

from tinydb import TinyDB, Query
from werkzeug import secure_filename
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from jsonrpc import JSONRPCResponseManager, Dispatcher

'''
This class opens a connection for nodes to register on using RPC
'''

ip = None
port = None
db = TinyDB('db.json')
nodes_db = db.table('nodes', cache_size=0)
ledger_db = db.table('ledger', cache_size=0)

class RPC(threading.Thread):

    def __init__(self, this_ip, this_port):
        threading.Thread.__init__(self)
        global ip, port
        ip = this_ip
        port = this_port


    def register_node(**kwargs):
        ip = kwargs["ip"]
        mac = kwargs["mac"]
        port = kwargs["port"]
        units = kwargs["units"]

        print("[!] New connection established with Node of MAC={} and IP={}".format(mac, ip))
        nodes_db.insert({'ip': ip, 'mac': mac, 'port': port, 'units': units})
        return { "code": 200, "msg": "Success." }


    def register_location(**kwargs):
        file_name = kwargs["file_name"]
        location = kwargs["location"] # Node mac
        print("[*] Adding {} to registry for file '{}'".format(location,
                                                               file_name))
        ledger_db.insert({'file_name': file_name, 'location': location})


    @Request.application
    def application(self, request):
        dispatcher = Dispatcher()
        dispatcher.add_method(RPC.register_node)
        dispatcher.add_method(RPC.register_location)
        response = JSONRPCResponseManager.handle(request.data, dispatcher)
        print("RPC server running... Ready to deploy!")
        return Response(response.json, mimetype='application/json')


    def run(self):
        run_simple(ip, port, self.application)
