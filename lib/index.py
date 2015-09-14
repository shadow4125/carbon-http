# -*- coding: utf-8 -*-
#
# Copyright @ 2015, Qunar OPSDEV
# 
# Author: shadow.zhang<shadowyue4125@gmail.com>

import os

from lib.conf import CONF
from lib.utils import rest


class Index(rest.QResource):

    def get(self):
        return "Welcome to carbon-http..."


class HealthCheck(rest.QResource):

    def get(self):
        if os.path.isfile(CONF.path.healthcheck):
            return "OK"
        return ("404", 404)
