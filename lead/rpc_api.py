import os
import time
import json
import errno
import threading

from node import Node

from subprocess import call
from tinydb import TinyDB, Query
from werkzeug import secure_filename
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from jsonrpc import JSONRPCResponseManager, dispatcher

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


    @dispatcher.add_method
    def register_node(**kwargs):
        f = open("log.txt", "a+")
        ip = kwargs["ip"]
        mac = kwargs["mac"]
        port = kwargs["port"]
        units = kwargs["units"]
        f.write("{};[!] New connection established with Node of MAC={} and IP={}\n".format(int(round(time.time() * 1000)),mac, ip))
        if(db.search(Query().mac == mac)):
            f.write("{}; Updating node MAC={} in db\n".format(int(round(time.time() * 1000)),mac))
            nodes_db.update({'mac': mac, 'ip': ip, 'port': port, 'units': units}, Query().mac == mac)
            f.write("{}; db for MAC={} updated\n".format(int(round(time.time() * 1000)),mac))
        else:
            f.write("{}; Adding node MAC={} to db\n".format(int(round(time.time() * 1000)),mac))
            nodes_db.insert({'mac': mac, 'ip': ip, 'port': port, 'units': units})
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
        ledger_db.insert({'file_name': file_name, 'location': location})
        f.write("{}; File ({}) for MAC={} add to register".format(int(round(time.time() * 1000)),location, file_name))
        f.close()

    @Request.application
    def application(self, request):
        response = JSONRPCResponseManager.handle(request.data, dispatcher)
        print("RPC server running... Ready to deploy!")
        # call([os.getcwd() + '/deploy.sh'])
        return Response(response.json, mimetype='application/json')


    def run(self):
        run_simple(ip, port, self.application)
