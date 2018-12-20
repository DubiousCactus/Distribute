import os
import json
import errno

from node import Node
from subprocess import call
from werkzeug import secure_filename
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
controller = None
ip = None
port = None


class REST_Internal():

    def __init__(self, ctrl, host, p):
        global controller, ip, port
        controller = ctrl
        ip = host
        port = p


    @app.route('/register/node', methods=['POST'])
    def register_node():
        ip = request.node.ip
        mac = request.node.mac
        print("[!] New connection established with Node of MAC={} and IP={}".format(mac, ip))
        if request.node.version > controller._version:
            controller.update_node(ip)
            return { "code": 200, "msg": "Updating slave..." }
        else:
            controller.add_node(ip, mac, request.node.port, request.node.units)
            return { "code": 200, "msg": "Success." }


    @app.route('/register/location', methods=['POST'])
    def register_location():
        file_name = request.file_name
        location = request.location # Node mac
        print("[*] Adding {} to registry for file '{}'".format(location,
                                                               file_name))
        controller.add_to_ledger(file_name, location)


    def start(self):
        app.run(debug=True, host=ip, port=port)
