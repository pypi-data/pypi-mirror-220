import json
from dataclasses import dataclass

import aio_pika
from aio_pika.abc import DeliveryMode, ExchangeType


@dataclass(slots=True)
class Emitter:
    rabbitmq_url: str

    async def emit(self, event_name: str, payload: dict) -> None:
        connection = await aio_pika.connect(self.rabbitmq_url)

        async with connection:
            channel = await connection.channel()
            await channel.declare_queue(event_name)

            exchange = await channel.declare_exchange(event_name, ExchangeType.FANOUT)
            body = json.dumps(payload, default=str)
            await exchange.publish(
                aio_pika.Message(body=str.encode(body), delivery_mode=DeliveryMode.PERSISTENT),
                routing_key=event_name,
            )
