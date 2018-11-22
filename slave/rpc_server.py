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

from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from jsonrpc import JSONRPCResponseManager, dispatcher


class Server:

    def __init__(self, controller, ip, port):
        self.controller = controller
        run_simple(ip, port, self.application)


    def success():
        return {"code": 200, "msg": "Success"}


    def failure():
        return {"code": 401, "msg": "Failure"}


    @dispatcher.add_method
    def write_file(**kwargs):
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


    @dispatchwer.add_method
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

