import logging

from kombu.transport.redis import Channel, Transport
from redis.sentinel import Sentinel, SentinelManagedConnection

logger = logging.getLogger(__name__)


class SentinelChannel(Channel):
    """
    Redis Channel for interacting with Redis Sentinel
    .. note::
        In order to correctly configure the sentinel,
        this channel expects specific broker transport options to be
        provided via ``BROKER_TRANSPORT_OPTIONS``.
        Here is are sample transport options::
            BROKER_TRANSPORT_OPTIONS = {
                'sentinels': [('192.168.1.1', 26379),
                              ('192.168.1.2', 26379),
                              ('192.168.1.3', 26379)],
                'service_name': 'master',
                'socket_timeout': 0.1,
            }
    """
    from_transport_options = Channel.from_transport_options + (
        'sentinels',
        'service_name',
        'socket_timeout',
        'min_other_sentinels',
        'password',
    )

    connection_class = SentinelManagedConnection

    def _sentinel_managed_pool(self, asynchronous=False):
        """
        Cached property for getting connection pool to redis sentinel.
        In addition to returning connection pool, this property
        changes the ``Transport`` connection details to match the
        connected master so that celery can correctly log to which
        node it is actually connected.
        Returns
        -------
        CelerySentinelConnectionPool
            Connection pool instance connected to redis sentinel
        """
        connparams = self._connparams(asynchronous)
        additional_params = connparams.copy()

        additional_params.pop('host', None)
        additional_params.pop('port', None)

        sentinels = getattr(self, 'sentinels', [])

        if not sentinels:
            sentinels.append((connparams['host'], connparams['port']))

        additional_params.update({
            'socket_timeout': getattr(self, 'socket_timeout', 0.1),
            'password': getattr(self, 'password', None)
        })

        sentinel = Sentinel(
            sentinels,
            min_other_sentinels=getattr(self, 'min_other_sentinels', 0),
            **additional_params
        )

        service_name = getattr(self, 'service_name', None)

        return sentinel.master_for(
            service_name,
            self.Client,
        ).connection_pool

    def _get_pool(self, asynchronous=False):
        return self._sentinel_managed_pool()


class SentinelTransport(Transport):
    """
    Redis transport with support for Redis Sentinel.
    """
    Channel = SentinelChannel
