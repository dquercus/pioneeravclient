#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'David Encinas Fernández'
__email__ = 'david@david'
__version__ = '0.1.0'

from clients import *

class PioneerAvClient(object):
    """ Factory pattern for client instantiation """

    @classmethod
    def factory(cls, model, ip, port=8102, timeout=10):
        """ Factory method that returns right client based on given model name. """
        if (model == "VSX-528"):
            return VSX528Telnet(ip,port)
        elif (model == "VSX-822"):
            return VSX528Telnet(ip,port)
        elif (model == "VSX-1023"):
            return VSX528Telnet(ip,port)
        elif (model == "VSX-921"):
            return VSX528Telnet(ip,port)
        else:
            PioneerAvClientException("Unsupported Pioneer AV Model")