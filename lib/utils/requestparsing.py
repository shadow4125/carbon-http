# -*- coding: utf-8 -*-
#
# Copyright @ 2015, Qunar OPSDEV
# 
# Author: shadow.zhang<shadowyue4125@gmail.com>

from flask import request


class RequestParams(object):

    def __getitem__(self, key):
        if request.json and key in request.json:
            return request.json[key]
        if key in request.form:
            return request.form.getlist(key)[-1]
        if key in request.args:
            return request.args.getlist(key)[-1]
        raise KeyError

    def __contains__(self, key):
        try:
            self[key]
            return True
        except KeyError:
            return False

    def get_header(self, key):
        headers = request.headers
        try:
            return headers[key]
        except KeyError:
            return None

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def getlist(self, key):
        if request.json and key in request.json:
            value = self[key]
            if not isinstance(value, list):
                value = [value]
            return value
        if key in request.form:
            return request.form.getlist(key)
        return request.args.getlist(key)

RequestParams = RequestParams()
