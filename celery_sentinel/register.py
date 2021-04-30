from kombu.transport import TRANSPORT_ALIASES

from .transport import SentinelTransport


def get_class_path(cls):
    return '{}.{}'.format(cls.__module__, cls.__name__)


def register(alias='redis-sentinel'):
    TRANSPORT_ALIASES[alias] = get_class_path(SentinelTransport)
