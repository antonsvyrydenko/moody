#!/usr/bin/env python
# coding: utf-8
import json
import os
import sys
import time

from kafka import KafkaProducer


if len(sys.argv) < 2:
    print('Please pass your mood')
    exit(1)

producer = KafkaProducer(
    bootstrap_servers=[os.environ['KAFKA_SERVER']],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

producer.send(
    os.environ['KAFKA_TOPIC'],
    value={'action': 'handle_mood', 'mood': sys.argv[1]}
)

time.sleep(2)
