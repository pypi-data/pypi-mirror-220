import logging

from confluent_kafka import Producer, SerializingProducer
from confluent_kafka.serialization import StringSerializer

from ronds_sdk import error
from ronds_sdk.options.pipeline_options import KafkaOptions
from ronds_sdk.tools.utils import Singleton


logger = logging.getLogger("executor")


class KafkaManager(metaclass=Singleton):

    # noinspection SpellCheckingInspection
    def __init__(self,
                 options,  # type: KafkaOptions
                 ):
        # type: (...) -> KafkaManager
        conf = {
            'bootstrap.servers': options.kafka_bootstrap_servers,
            'acks': -1,
            'request.timeout.ms': 180000,
            'linger.ms': 1000,
            'key.serializer': StringSerializer('utf_8'),
            'value.serializer': StringSerializer('utf_8'),
            'message.max.bytes': 10000000
        }
        self.send_kafka_mock = options.kafka_send_mock
        self.producer = SerializingProducer(conf)

    def send(self,
             topic,  # type: str
             key,  # type: str,
             value,  # type: str
             ):
        if self.send_kafka_mock:
            logger.info('topic: %s, key: %s, value: %s' % (topic, key, value))
        else:
            self.producer.produce(
                topic,
                key=key,
                value=value,
            )
            self.producer.poll(10)

    def __del__(self):
        if self.producer is not None:
            self.producer.flush()
            self.producer = None


def acked(err, msg):
    if err is not None:
        err_msg = "Failed to deliver message: %s: %s" % (str(msg), str(err))
        logger.error(err_msg)
        raise error.KafkaError(err_msg)
