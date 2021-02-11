#!/usr/bin/env python


""" class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
"""


def serializeReportContent(obj):
    """JSON serializer for objects not serializable by default json code"""

    return {_: getattr(obj, _) for _ in dir(obj) if not _.startswith("_")}
