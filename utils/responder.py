#!/usr/bin/env python
# coding: utf-8
import json
import os
import time

from typing import Tuple

from loguru import logger
from kafka import KafkaProducer


class Responder:
    def __init__(self) -> None:
        self.kafka_server = os.environ['KAFKA_SERVER']
        self.topic_name = os.environ['KAFKA_TOPIC']

    def _send_message(self, data: Tuple) -> None:
        logger.info(
            f'Sending back mood handler:'
            f'\n{json.dumps(data, indent=4)}'
        )

        message = {
            'action': 'solve_mood',
            'solution': data[0],
            'mood': data[1],
        }

        producer = KafkaProducer(
            bootstrap_servers=[self.kafka_server],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        producer.send(self.topic_name, value=message)
        time.sleep(2)

    def run(self, data: Tuple) -> None:
        self._send_message(data)
