#! /usr/bin/python3

import os
import json
import errno

from node import Node
from subprocess import call
from werkzeug import secure_filename
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from flask import Flask, render_template, request
from jsonrpc import JSONRPCResponseManager, dispatcher
import rest_api
import rpc_api

app = Flask(__name__)

class LeadNode:
    def __init__(self, config):
        self.api_addr = config['api_addr']
        self.rpc_addr = config['rpc_addr']
        self.api_port = config['api_port']
        self.rpc_port = config['rpc_port']
        self._version = config['version']
        self.nodes = []

if __name__ == '__main__':
    with open('config.json', 'r') as config_file:
        leadNode = LeadNode(config_file)
        rest = rest_api(self.nodes,self.api_addr,self.api_port)
        rpc = rest_api(self.nodes,self.rpc_addr,self.rpc_port,self.version)
        rest.start()
        rpc.start()
