from __future__ import absolute_import

__version__ = "3.6.1"


def get_instance():
    from . import instance

    return instance.instance
