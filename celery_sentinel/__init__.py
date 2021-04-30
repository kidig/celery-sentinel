__author__ = "Dmitry Gerasimenko"
__version__ = "0.0.1"


try:
    from .celery import Celery  # noqa
except ImportError:
    pass
