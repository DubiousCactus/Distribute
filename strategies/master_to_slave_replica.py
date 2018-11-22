#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 theomorales <theomorales@Theos-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.

"""
Master to slave using replication
"""

from . import Strategy


class Master_to_slave_replica(Strategy):
    def __init__(self, controller, desc, nb_replicas, losses):
        Strategy.__init__(self, desc)
        self.nb_replicas = nb_replicas
        self.losses = losses

    def store_file(self, file_bytes, file_name):
        pass

    def retreive_file(self, file_name):
        pass

    def get_time(self):
        pass
