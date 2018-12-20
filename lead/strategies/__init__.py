#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#
# Distributed under terms of the MIT license.

"""
Module init file
"""

from importlib import import_module

from .strategy_base import Strategy


def get(strategy_name, controller, *args, **kwargs):
    try:
        module_name = strategy_name
        class_name = strategy_name.capitalize()
        strategy_module = import_module('.' + module_name, package='strategies')
        strategy_class = getattr(strategy_module, class_name)
        instance = strategy_class(controller, *args, **kwargs)

    except (AttributeError, ModuleNotFoundError):
        raise ImportError('{} is not part of the strategy collection!'.format(strategy_name))
    else:
        if not issubclass(strategy_class, Strategy):
            raise ImportError("{} is currently not implemented.".format(strategy_class))




    return instance

