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

import os

from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from jsonrpc import JSONRPCResponseManager, dispatcher


class Server:

    def __init__(self, controller, ip, port):
        self.controller = controller
        run_simple(ip, port, application)

    @dispatcher.add_method
    def write_file(**kwargs):
        with open("~/storage/{}".format(kwargs['filename']), 'wb') as file:
            file.write(kwargs["bytes"])
            return "success"

        return "failure"

    @dispatcher.add_method
    def read_file(**kwargs):
        return self.controller.read_file(kwargs["filename"])

    @dispatcher.add_method
    def delete_file(**kwargs):
        os.remove(kwargs["filename"])
        return "success"

    @Request.application
    def application(request):
        response = JSONRPCResponseManager.handle(request.data, dispatcher)
        print(request.data)
        return Response(response.json,mimetype='application/json')

