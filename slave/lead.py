#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 theomorales <theomorales@Theos-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.

"""
Lead node client class
"""

from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from jsonrpc import JSONRPCResponseManager, dispatcher


class LeadNode:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def call(self, payload):
        url = "http://{}:{}".format(self.leadIP, self.leadPort)
        headers = {'content-type': 'application/json'}
        return requests.post(url, data=json.dumps(payload), headers=headers).json()


