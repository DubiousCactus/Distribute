#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 theomorales <theomorales@Theos-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.

"""
Node class for the LeadNode project
"""

class Node:
    def __init__(self, id, mac, ip):
        self.id = id
        self.mac = mac
        self.ip = ip
        self.storage_units = 1


    def set_storage_units(self, nb_units):
        self.storage_units = nb_units


    def write(self, file):
        pass


    def read(self, fileName):
        pass
