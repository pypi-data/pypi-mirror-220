from django.core.management.base import BaseCommand
from kfsd.apps.core.msmq.rabbitmq.base import RabbitMQ


class Command(BaseCommand):
    help = "Listens to a RabbitMQ topic"

    def handle(self, *args, **options):
        msmqHandler = RabbitMQ()
        self.__config = msmqHandler.getConfig()
        exchangeName = "test_exchange"
        queueName = "test_queue"
        routingKey = "test_routing"

        msmqHandler.publish_msg(
            exchangeName, queueName, routingKey, "hi this is my first msg"
        )

        def callback(ch, method, properties, body):
            print("Msg Body: {}".format(body))

        msmqHandler.consume_msgs(callback, exchangeName, queueName, routingKey)
