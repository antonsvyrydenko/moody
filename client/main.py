#!/usr/bin/env python
# coding: utf-8
import json
import os

from loguru import logger
from kafka import KafkaConsumer


class ResultListener:
    def __init__(self) -> None:
        self.kafka_server = os.environ['KAFKA_SERVER']
        self.kafka_topic = os.environ['KAFKA_TOPIC']

    def run(self) -> None:
        consumer = KafkaConsumer(
            self.kafka_topic,
            bootstrap_servers=[self.kafka_server],
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        logger.debug(
            f"Listening {self.kafka_topic}@{self.kafka_server}..."
        )

        for message in consumer:
            transmission = message.value

            if transmission['action'] == 'solve_mood':
                logger.success(
                    f'If you are {transmission["mood"]}, '
                    f'here are my words for you: "{transmission["solution"]}"'
                )

if __name__ == '__main__':
    listener = ResultListener()
    listener.run()
