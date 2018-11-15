#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 theomorales <theomorales@Theos-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.

"""
Slave to slave with coding
"""

from . import Strategy


class Slave_to_slave_coded(Strategy):
    def __init__(self, desc, losses):
        Strategy.__init__(self, desc)
        self.losses = losses

    def store_file(self, file_bytes, file_name):
        pass

    def retreive_file(self, file_name):
        pass

    def get_time(self):
        pass
