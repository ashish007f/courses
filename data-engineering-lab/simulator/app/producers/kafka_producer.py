import json
from typing import Any
from aiokafka import AIOKafkaProducer
from .base import EventProducer
from ..core.config import settings

class KafkaEventProducer(EventProducer):
    def __init__(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            key_serializer=lambda k: k.encode('utf-8') if isinstance(k, str) else str(k).encode('utf-8'),
            value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')
        )

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send_event(self, topic: str, key: str, value: Any):
        await self.producer.send_and_wait(topic, value, key=key)
