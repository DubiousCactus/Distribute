#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 theomorales <theomorales@Theos-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.

"""
Strategy base class
"""

from abc import ABCMeta, abstractmethod


class Strategy(object):
    def __init__(self, controller, description=None):
        self.description = description
        self.controller = controller

    @abstractmethod
    def store_file(self, file_bytes, file_name):
        pass

    @abstractmethod
    def retrieve_file(self, file_name, locations):
        pass

    @abstractmethod
    def get_time(self):
        pass
