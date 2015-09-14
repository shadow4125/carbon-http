# -*- coding: utf-8 -*-
#
# Copyright @ 2015, Qunar OPSDEV
# 
# Author: shadow.zhang<shadowyue4125@gmail.com>

from qg.core import log as logging

LOG = logging.getLogger(__name__)


class Metric(object):

    def __init__(self, metric_dict):
        if self.valid(metric_dict):
            self.metric = metric_dict
        else:
            raise ValueError('Invalid Metric')

    def valid(self, metric_dict):
        for key in ('metric', 'value', 'timestamp'):
            if key not in metric_dict:
                return False
        return True

    def enqueue(self, queue):
        try:
            queue.put((self.metric['metric'], (self.metric['timestamp'], self.metric['value'])), block=True, timeout=1)
        except Exception:
            LOG.warning('Send queue full: dropping metric - %s %f %f' % (
                self.metric['metric'],
                self.metric['value'],
                self.metric['timestamp']
            ))
