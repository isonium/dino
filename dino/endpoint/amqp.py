from kombu import pools
pools.set_limit(1024)  # default is 200

from dino.config import ConfigKeys
from dino.endpoint.base import BasePublisher

from kombu import Exchange
from kombu import Queue
from kombu import Connection

import logging

logger = logging.getLogger(__name__)


class AmqpPublisher(BasePublisher):
    def __init__(self, env, is_external_queue: bool, fanout: bool=True):
        super().__init__(env, is_external_queue, queue_type='amqp', logger=logger)
        conf = env.config

        queue_host = conf.get(ConfigKeys.HOST, domain=self.domain_key, default='')
        if queue_host is None or len(queue_host.strip()) == 0:
            return

        queue_port = conf.get(ConfigKeys.PORT, domain=self.domain_key, default=None)
        queue_vhost = conf.get(ConfigKeys.VHOST, domain=self.domain_key, default=None)
        queue_user = conf.get(ConfigKeys.USER, domain=self.domain_key, default=None)
        queue_pass = conf.get(ConfigKeys.PASSWORD, domain=self.domain_key, default=None)

        queue_host = ';'.join(['amqp://%s' % host for host in queue_host.split(';')])
        queue_exchange = '%s_%s' % (
            conf.get(ConfigKeys.EXCHANGE, domain=self.domain_key, default=None),
            conf.get(ConfigKeys.ENVIRONMENT)
        )
        direct_exchange = 'direct_{}'.format(queue_exchange)

        bind_port = self.get_port()
        if bind_port is None:
            logging.info('skipping pubsub setup, no port specified')
            return

        self.queue_name = conf.get(ConfigKeys.QUEUE, domain=self.domain_key, default=None)
        if self.queue_name is None or len(self.queue_name.strip()) == 0:
            self.queue_name = '{}node_queue_{}_{}_{}'.format(
                '' if fanout else 'direct_',
                conf.get(ConfigKeys.ENVIRONMENT),
                self.get_host(),
                bind_port
            )

        if self.is_external_queue:
            self.exchange = Exchange(queue_exchange, type='direct')
        else:
            if fanout:
                self.exchange = Exchange(queue_exchange, type='fanout')
            else:
                self.exchange = Exchange(direct_exchange, type='direct')

        self.queue_connection = Connection(
            hostname=queue_host,
            port=queue_port,
            virtual_host=queue_vhost,
            userid=queue_user,
            password=queue_pass
        )
        if fanout:
            self.queue = Queue(self.queue_name, self.exchange)
        else:
            self.queue = Queue(self.queue_name, self.exchange, routing_key=self.queue_name)

        self.logger.info('setting up pubsub for type "{}: and host(s) "{}"'.format(self.queue_type, queue_host))

    def get_direct_queue(self, queue_name, exchange):
        return Queue(queue_name, self.exchange, routing_key=queue_name)
