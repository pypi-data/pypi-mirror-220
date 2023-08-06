from django.core.management.base import BaseCommand
from kfsd.apps.core.msmq.rabbitmq.base import RabbitMQ
from kfsd.apps.core.utils.time import Time
from kfsd.apps.endpoints.serializers.common.outpost import (
    MsgSerializer,
    OutpostModelSerializer,
)
from kfsd.apps.core.common.logger import Logger, LogLevel
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.models.tables.outpost import Outpost, send_msg
from kfsd.apps.models.constants import (
    SERVICE_CONFIG_ID_REMIND,
    COMMON_ACTION_OUTPOST_CLEAR,
    REMIND_ACTION_CREATE,
    REMIND_ACTION_IN_MINS,
)

import json

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


def send_clear_outpost_reminder(config, serviceConfigId):
    identifier = "ORG=Kubefacets,APP={},TYPE=Outpost,Action=Clear".format(
        serviceConfigId
    )
    clientExchangeName, clientQueueName, clientRoutingKey = get_service_msmq_details(
        config, serviceConfigId
    )
    remindExchangeName, remindQueueName, remindRoutingKey = get_service_msmq_details(
        config, SERVICE_CONFIG_ID_REMIND
    )
    outpostData = {
        "msg_queue_info": {
            "exchange_name": remindExchangeName,
            "queue_name": remindQueueName,
            "routing_key": remindRoutingKey,
        },
        "msg": {
            "action": REMIND_ACTION_CREATE,
            "data": {
                "identifier": identifier,
                "type": "REPEAT",
                "remind_by_in_mins": REMIND_ACTION_IN_MINS,
                "to_msg_queue": {
                    "exchange_name": clientExchangeName,
                    "queue_name": clientQueueName,
                    "routing_key": clientRoutingKey,
                },
                "msg": {
                    "action": COMMON_ACTION_OUTPOST_CLEAR,
                    "data": {"identifier": identifier},
                },
            },
        },
    }
    outpostSerializer = OutpostModelSerializer(data=outpostData)
    outpostSerializer.is_valid(raise_exception=True)
    outpostSerializer.save()


def get_service_msmq_details(config, serviceConfigId):
    return config.findConfigs(
        [
            "services.rabbitmq.consume.{}.exchange_name".format(serviceConfigId),
            "services.rabbitmq.consume.{}.queue_name".format(serviceConfigId),
            "services.rabbitmq.consume.{}.routing_key".format(serviceConfigId),
        ]
    )


def clear_outpost(data):
    logger.info("Recd CLEAR_OUTPOST command on msmq")
    outpostQS = Outpost.objects.all()
    for outpostIns in outpostQS:
        send_msg(outpostIns.id)


callback_map = {COMMON_ACTION_OUTPOST_CLEAR: clear_outpost}


def base_callback(ch, method, properties, body):
    bodyStr = body.decode().replace("'", '"')
    jsonStr = json.loads(bodyStr)
    serializedData = MsgSerializer(data=jsonStr)
    serializedData.is_valid(raise_exception=True)

    action = DictUtils.get(serializedData.data, "action")
    callback_map[action](serializedData.data)


class Command(BaseCommand):
    help = "Listens to a RabbitMQ topic"

    def __init__(self, callbackFn=base_callback):
        self.__callbackFn = callbackFn

    def add_arguments(self, parser):
        parser.add_argument(
            "-s",
            "--service_config_id",
            type=str,
            help="Service Config Id",
        )

    def connectToMSMQ(self):
        try:
            msmqHandler = RabbitMQ()
            return msmqHandler
        except Exception:
            logger.error(
                "Error connecting to RabbitMQ, check if RabbitMQ instance is up!"
            )
            Time.sleep(30)
            self.connectToMSMQ()

    def consumeMsgs(self, serviceConfigId, config, msmqHandler):
        exchangeName, queueName, routingKey = get_service_msmq_details(
            config, serviceConfigId
        )
        logger.info(
            "Listening msgs at exchange: {}, queue: {}, routing key: {}".format(
                exchangeName, queueName, routingKey
            )
        )
        msmqHandler.consume_msgs(self.__callbackFn, exchangeName, queueName, routingKey)

    def handle(self, *args, **options):
        logger.info("Listening to MSMQ messages...")
        serviceConfigId = DictUtils.get(options, "service_config_id")
        msmqHandler = self.connectToMSMQ()
        config = msmqHandler.getConfig()
        send_clear_outpost_reminder(config, serviceConfigId)
        self.consumeMsgs(serviceConfigId, config, msmqHandler)
