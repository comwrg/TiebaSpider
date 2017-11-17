# -*- coding: utf-8 -*-
"""
wrapper
~
装饰器
:copyright: (c) 2017 by comwrg.
:license: MIT, see LICENSE for more details.
"""
import types


def ignore_exception(*exceptions):
    """Usage:
    @ignore_exception(EOFError, "NameError")
    support type string and type Exception

    :param exceptions: string or Exception
    """
    def decorate(func):
        def call(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception, e:
                for item in exceptions:
                    if isinstance(item, str) and item in e.message:
                        return
                    if type(e) is item:
                        return
                    raise
        return call
    return decorate
