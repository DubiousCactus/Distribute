#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 theomorales <theomorales@Theos-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.

"""
RPC Server used to receive instructions from the lead node
"""

import threading

from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from jsonrpc import JSONRPCResponseManager, dispatcher


controller = None
ip = None
port = None

class Server(threading.Thread):

    def __init__(self, controller, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.controller = controller


    def run(self):
        run_simple(self.ip, self.port, self.application)


    def success():
        return {"code": 200, "msg": "Success"}


    def failure():
        return {"code": 401, "msg": "Failure"}


    @dispatcher.add_method
    def write_file(**kwargs):
        print("writing file")
        print(kwargs["name"])
        print(kwargs["content"])
        file = open(kwargs["name"], "w")
        file.write(kwargs["content"].decode('hex'))
        file.close()
        if self.controller.write(kwargs["name"], kwargs["content"]):
            return success()
        else:
            return failure()


    @dispatcher.add_method
    def write_file_repeat(**kwargs):
        if self.controller.write(kwargs["name"], kwargs["content"]):
            if kwargs["ttl"] > 0:
                if self.controller.pick_and_repeat(
                        kwargs["name"],
                        kwargs["content"],
                        kwargs["ttl"]
                    ):
                    return success()
                else:
                    return failure()
        else:
            return failure()


    @dispatcher.add_method
    def read_file(**kwargs):
        return self.controller.read_file(kwargs["name"])


    @dispatcher.add_method
    def delete_file(**kwargs):
        if self.controller.delete(kwargs["name"]):
            return success()
        else:
            return failure()


    @dispatcher.add_method
    def add_neighbour(**kwargs):
        if self.controller.add_neighbour(
            kwargs["mac"], kwargs["ip"], kwargs["port"], kwargs["units"]
        ):
            return success()
        else:
            return failure()

    @Request.application
    def application(self, request):
        response = JSONRPCResponseManager.handle(request.data, dispatcher)
        return Response(response.json, mimetype='application/json')

