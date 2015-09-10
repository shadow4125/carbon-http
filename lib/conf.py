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
