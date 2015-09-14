# -*- coding: utf-8 -*-
#
# Copyright @ 2015, Qunar OPSDEV
# 
# Author: shadow.zhang<shadowyue4125@gmail.com>

import threading
import Queue
import signal
import time
import sys

from qg.core.app.exts.log import QLogExtension
from qg.core import log as logging
from qg.web.app import QFlaskApplication

from lib.conf import CONF
from lib.utils import rest
from lib.sender import CarbonSender

LOG = logging.getLogger(__name__)


class CarbonHttpApplication(QFlaskApplication, rest.QRestfulMixin):
    name = 'carbon-http'
    version = '1.0'

    def signal_handler(self, signum, frame):
        self.carbon_sender.is_running = False

        # 等待sender线程退出
        for t in threading.enumerate():
            if t.getName() == 'MainThread':
                continue

            if type(t) is CarbonSender:
                cnt = 3
                while cnt > 0:
                    if not t.isAlive():
                        break
                    cnt = cnt - 1
                    time.sleep(1)

        # 退出主进程
        sys.exit(0)

    def configure(self):
        super(CarbonHttpApplication, self).configure()

        self.queue = Queue.Queue(CONF.queue.maxsize)

        # start sender worker thread
        self.carbon_sender = CarbonSender(self.queue, CONF.carbon.host, CONF.carbon.port)
        self.carbon_sender.start()

        # handler the signal
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def init_flask_app(self):
        super(CarbonHttpApplication, self).init_flask_app()
        self.register_extension(QLogExtension())

        for mixin in self.__class__.__bases__:
            if hasattr(mixin, 'flask_mixin_init'):
                getattr(mixin, 'flask_mixin_init')(self)

        # restful resources
        from lib import index
        from lib import publish

        self.add_resource(index.Index, '/')
        self.add_resource(index.HealthCheck, '/healthcheck.html')
        self.add_resource(publish.Normal, '/publish/normal')
        self.add_resource(publish.Batch, '/publish/batch')
        self.add_resource(publish.Jsonp, '/publish/jsonp')


carbon_http_entry = CarbonHttpApplication().make_entry_point()
