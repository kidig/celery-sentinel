from celery import Celery as _Celery
from .register import register


register()


class Celery(_Celery):
    pass
