#!/usr/bin/env python
# coding: utf-8
import json
import os

from typing import Tuple

from loguru import logger
from kafka import KafkaConsumer

from utils.responder import Responder
from utils.mood_handler import MoodHandler


class MoodListener:
    def __init__(self) -> None:
        self.kafka_server = os.environ['KAFKA_SERVER']
        self.kafka_topic = os.environ['KAFKA_TOPIC']

        self.responder = Responder()
        self.mood_handler = MoodHandler()

        self.moods = {
            'sad': self.mood_handler.handle_sad,
            'upset': self.mood_handler.handle_upset,
            'happy': self.mood_handler.handle_happy,
            'angry': self.mood_handler.handle_angry,
            'curious': self.mood_handler.handle_curious
        }

    @staticmethod
    def _return_mood_reaction(result: Tuple) -> None:
        Responder().run(result)

    def run(self) -> None:
        consumer = KafkaConsumer(
            self.kafka_topic,
            bootstrap_servers=[self.kafka_server],
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            group_id='moody_consumer'
        )

        logger.debug(
            f"Listening {self.kafka_topic}@{self.kafka_server}..."
        )

        for message in consumer:
            transmission = message.value

            logger.debug('Received message:')
            logger.info(f'\n{json.dumps(transmission, indent=4)}')

            if transmission['action'] == 'handle_mood':
                handle_mood = self.moods.get(transmission['mood'])
                if not handle_mood:
                    result = "Can't help with your mood", transmission['mood']
                else:
                    result = handle_mood(), transmission['mood']
                self._return_mood_reaction(result)

                logger.debug("DONE")

if __name__ == '__main__':
    listener = MoodListener()
    listener.run()
