# -*- coding: utf-8 -*-
#
# Copyright @ 2015, Qunar OPSDEV
# 
# Author: shadow.zhang<shadowyue4125@gmail.com>

from qg.core.exception import QException


class CException(QException):
    message = 'Web Error.'
    errcode = 99

    def __init__(self, *args, **kwargs):
        super(CException, self).__init__(*args, **kwargs)
        self.data = {
            "message": self.message,
            "errcode": self.errcode
        }


class CParamsMissing(CException):
    code = 400
    message = 'Param Missing.'


class CParamsError(CException):
    code = 400
    message = 'Param Error.'
