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
import time
import sys
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
        f = open("log.txt", "a+")
        ip = kwargs["ip"]
        mac = kwargs["mac"]
        port = kwargs["port"]
        units = kwargs["units"]
        f.write("{};[!] New connection established with Node of MAC={} and IP={}\n".format(int(round(time.time() * 1000)),mac, ip))
        if(kwargs["version"] > controller._version):
            f.write("{}; Updating code on node with MAC={]\n".format(int(round(time.time() * 1000)),mac))
            call([os.getcwd() + '/deploy.sh', ip])
            f.write("{}; Node MAC={} updated\n".format(int(round(time.time() * 1000)),mac))
            sys.stdout.close()
            f.close()
            return { "code": 200, "msg": "Updating slave..." }
        else:
            if(db.search(Query().mac == mac)):
                f.write("{}; Updating node MAC={} in db\n".format(int(round(time.time() * 1000)),mac))
                db.update({'mac': mac, 'ip': ip, 'port': port, 'units': units}, Query().mac == mac)
                f.write("{}; db for MAC={} updated\n".format(int(round(time.time() * 1000)),mac))
            else:
                f.write("{}; Adding node MAC={} to db\n".format(int(round(time.time() * 1000)),mac))
                db.insert({'mac': mac, 'ip': ip, 'port': port, 'units': units})
                f.write("{}; MAC={} Added to db\n".format(int(round(time.time() * 1000)),mac))
            f.close()
            return { "code": 200, "msg": "Success." }

    @dispatcher.add_method
    def register_location(**kwargs):
        f = open("log.txt", "a+")
        file_name = kwargs["file_name"]
        location = kwargs["location"]  # Node mac
        size = kwargs["size"]
        f.write("{}; Adding MAC={} to registry for file '{}'".format(int(round(time.time() * 1000)),location, file_name))
        controller.add_to_ledger(file_name, location, size)
        f.write("{}; File ({}) for MAC={} add to register".format(int(round(time.time() * 1000)),location, file_name))
        f.close()

    @Request.application
    def application(self, request):
        response = JSONRPCResponseManager.handle(request.data, dispatcher)
        return Response(response.json, mimetype='application/json')




    def run(self):
        run_simple(ip, port, self.application)
