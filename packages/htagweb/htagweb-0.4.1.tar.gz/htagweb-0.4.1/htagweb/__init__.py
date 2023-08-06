# -*- coding: utf-8 -*-
# #############################################################################
# Copyright (C) 2023 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/htagweb
# #############################################################################

from .webbase import WebServer
from .webbase import WebServerWS

from .htagserver import HtagServer  # a completly different beast.

__all__= ["WebServer","WebServerWS","HtagServer"]

__version__ = "0.4.1" # auto updated
