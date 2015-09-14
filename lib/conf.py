# -*- coding: utf-8 -*-
#
# Copyright @ 2015, Qunar OPSDEV
# 
# Author: shadow.zhang<shadowyue4125@gmail.com>

from oslo_config import cfg

CONF = cfg.CONF

CONF.register_opts([
    cfg.StrOpt('healthcheck', default='')
], 'path')

CONF.register_opts([
    cfg.StrOpt('host', default='127.0.0.1'),
    cfg.IntOpt('port', default=2014)
], 'carbon')

CONF.register_opts([
    cfg.IntOpt('maxsize', default=1000)
], 'queue')
