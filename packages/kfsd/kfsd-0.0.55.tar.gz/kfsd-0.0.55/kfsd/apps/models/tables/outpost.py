from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import json

from kfsd.apps.models.base import BaseModel
from kfsd.apps.core.utils.system import System
from kfsd.apps.core.utils.time import Time
from kfsd.apps.core.msmq.rabbitmq.base import RabbitMQ
from kfsd.apps.core.common.logger import Logger, LogLevel


logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class Outpost(BaseModel):
    STATUS_CHOICES = (
        ("P", "PENDING"),
        ("I", "IN-PROGRESS"),
        ("E", "ERROR"),
        ("C", "COMPLETED"),
    )

    msg_queue_info = models.JSONField(default=dict)
    msg = models.JSONField(default=dict)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="P")
    attempts = models.IntegerField(default=0)
    debug_info = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.identifier = System.uuid(32)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = "models"
        verbose_name = "Outpost"
        verbose_name_plural = "Outpost"


@receiver(post_save, sender=Outpost)
def signal_send_msg(sender, instance, created, **kwargs):
    if created:
        send_msg(instance.id)


def send_msg(instance_id):
    instance = Outpost.objects.get(id=instance_id)
    exchangeName = instance.msg_queue_info["exchange_name"]
    queueName = instance.msg_queue_info["queue_name"]
    routingKey = instance.msg_queue_info["routing_key"]
    logger.info(
        "Sending msg for outpost id: {} to exchange: {}, queue: {}, routing key: {}".format(
            instance.identifier, exchangeName, queueName, routingKey
        )
    )
    try:
        rabbitMQ = RabbitMQ()
        rabbitMQ.publish_msg_and_close_connection(
            exchangeName,
            queueName,
            routingKey,
            json.dumps(instance.msg),
        )
        instance.delete()
    except Exception:
        oldDebugInfo = instance.debug_info
        currentTimeStr = Time.calculate_time(Time.current_time(), {"minutes": 0}, True)
        oldDebugInfo[currentTimeStr] = "Error occurred in publishing outpost msg"
        instance.debug_info = oldDebugInfo
        instance.attempts += 1
        instance.save()
