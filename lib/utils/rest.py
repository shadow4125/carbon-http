# -*- coding: utf-8 -*-
#
# Copyright @ 2015, Qunar OPSDEV
# 
# Author: shadow.zhang<shadowyue4125@gmail.com>

from flask.ext.restful import reqparse
import flask.ext.restful as flask_restful


class QResource(flask_restful.Resource):

    def make_succ(self, **kwargs):
        data = {}
        data.update(kwargs)
        return {
            "errcode": 0,
            "message": "success",
            "data": data
        }

    def make_fail(self, **kwargs):
        data = {}
        data.update(kwargs)
        return {
            "errcode": 999,
            "message": "failed",
            "data": data
        }

    def make_result(self, **kwargs):
        data = {}
        data.update(kwargs)
        return {
            "errcode": 0,
            "message": "success",
            "data": data
        }

    def make_parser(self):
        return reqparse.RequestParser(argument_class=QwrArgument)


class QRestfulMixin(object):

    def flask_mixin_init(self):
        app = self.flask_app
        self._restful_api = flask_restful.Api(app)

    def add_resource(self, *args, **kwargs):
        self._restful_api.add_resource(*args, **kwargs)


class QwrArgument(reqparse.Argument):
    def __init__(self, *args, **kwargs):
        # default config
        p_kwargs = {
            "required": True,
            "errcode": 99
        }
        p_kwargs.update(kwargs)
        self.errcode = p_kwargs["errcode"]
        del p_kwargs["errcode"]
        super(QwrArgument, self).__init__(*args, **p_kwargs)

    def handle_validation_error(self, error):
        message = self.help if self.help is not None else str(error)
        flask_restful.abort(400, errcode=self.errcode, message=message)
