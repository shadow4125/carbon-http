# -*- coding: utf-8 -*-
#
# Copyright @ 2015, Qunar OPSDEV
# 
# Author: shadow.zhang<shadowyue4125@gmail.com>


from qg.core.app.exts.log import QLogExtension
from qg.core import log as logging
from qg.web.app import QFlaskApplication

from utils import rest

LOG = logging.getLogger(__name__)


class CarbonHttpApplication(QFlaskApplication, rest.QRestfulMixin):
    name = 'carbon-http'
    version = '1.0'

    def init_flask_app(self):
        super(CarbonHttpApplication, self).init_flask_app()
        self.register_extension(QLogExtension())

        for mixin in self.__class__.__bases__:
            if hasattr(mixin, 'flask_mixin_init'):
                getattr(mixin, 'flask_mixin_init')(self)

        # restful resources
        from lib import index

        self.add_resource(index.Index, '/')
        self.add_resource(index.HealthCheck, '/healthcheck.html')


carbon_http_entry = CarbonHttpApplication().make_entry_point()
