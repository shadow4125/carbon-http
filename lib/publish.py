# -*- coding: utf-8 -*-
#
# Copyright @ 2015, Qunar OPSDEV
# 
# Author: shadow.zhang<shadowyue4125@gmail.com>

from lib.utils import rest
from lib.utils.requestparsing import RequestParams
from lib.utils.exception import (
    CParamsMissing,
    CParamsError
)
from lib.metric import Metric


class Normal(rest.QResource):

    def publish(self):
        if 'metric' not in RequestParams:
            raise CParamsMissing('Param %s is required' % 'metric')
        if 'value' not in RequestParams:
            raise CParamsMissing('Param %s is required' % 'value')
        if 'timestamp' not in RequestParams:
            raise CParamsMissing('Param %s is required' % 'timestamp')

        metric = RequestParams.get('metric')
        value = RequestParams.get('value')
        timestamp = RequestParams.get('timestamp')

        from lib import app
        app = app.CarbonHttpApplication()
        queue = app.queue

        try:
            m = Metric({
                'metric': metric,
                'value': value,
                'timestamp': timestamp
            })
            m.enqueue(queue)
            return self.make_result()
        except ValueError:
            raise CParamsError('Invalid Metric.')

    def get(self):
        return self.publish()

    def post(self):
        return self.publish()


class Batch(rest.QResource):

    def publish(self):
        if 'metrics' not in RequestParams:
            raise CParamsMissing('Param %s is required' % 'metrics')

        metrics = RequestParams.get('metrics')

        if type(metrics) != list:
            raise CParamsError('Param %s must be list' % 'metrics')

        from lib import app
        app = app.CarbonHttpApplication()
        queue = app.queue

        for metric_dict in metrics:
            try:
                m = Metric(metric_dict)
                m.enqueue(queue)
            except ValueError:
                raise CParamsError('Invalid Metric.')

        return self.make_result()

    def get(self):
        return self.publish()

    def post(self):
        return self.publish()


class Jsonp(rest.QResource):

    def publish(self):
        callback = RequestParams.get('callback', None)
        if callback is None:
            return '{0}({1})'.format(callback, {'msg': 'Param %s is required' % 'callback'})
        if 'metric' not in RequestParams:
            return '{0}({1})'.format(callback, {'msg': 'Param %s is required' % 'metric'})
        if 'value' not in RequestParams:
            return '{0}({1})'.format(callback, {'msg': 'Param %s is required' % 'value'})
        if 'timestamp' not in RequestParams:
            return '{0}({1})'.format(callback, {'msg': 'Param %s is required' % 'timestamp'})

        metric = RequestParams.get('metric')
        value = RequestParams.get('value')
        timestamp = RequestParams.get('timestamp')

        from lib import app
        app = app.CarbonHttpApplication()
        queue = app.queue

        try:
            m = Metric({
                'metric': metric,
                'value': value,
                'timestamp': timestamp
            })
            m.enqueue(queue)
        except ValueError:
            return '{0}({1})'.format(callback, {'msg': 'Invalid Metric.'})

        return '{0}({1})'.format(callback, {'msg': 'Publish success.'})

    def get(self):
        return self.publish()

    def post(self):
        return self.publish()
