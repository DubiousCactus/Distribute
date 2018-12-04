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

import json
import requests


class LeadNode:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def call(self, payload):
        url = "http://{}:{}".format(self.ip, self.port)
        headers = {'content-type': 'application/json'}

        return requests.post(url, data=json.dumps(payload), headers=headers).json()


