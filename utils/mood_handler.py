#!/usr/bin/env python
# coding: utf-8
import random
import requests

from typing import Union

from requests.models import Response
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from loguru import logger

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class MoodHandler:
    def __init__(self) -> None:
        pass

    @staticmethod
    def _send_request(url: str) -> Union[None,Response]:
        result = None
        try:
            result = requests.get(url,verify=False).json()
        except Exception as e:
            logger.error(f'Failed to get mood solution. {e}')
        return result

    def handle_sad(self) -> str:
        result = self._send_request('https://www.affirmations.dev/')
        return "Can't help with your mood" if not result \
            else result['affirmation']

    def handle_upset(self) -> str:
        result = self._send_request(
            'https://binaryjazz.us/wp-json/genrenator/v1/genre/5'
        )
        return "Can't help with your mood" if not result \
            else f'How about new music genre: {random.choice(result)}?'

    def handle_happy(self) -> str:
        result = self._send_request(
            'https://api.thecatapi.com/v1/images/search'
        )
        return "Can't help with your mood" if not result \
            else f'Take a look at these catpic: {result[0]["url"]}'

    def handle_angry(self) -> str:
        result = self._send_request(
            'https://abhi-api.vercel.app/api/fun/jdark'
        )
        return "Can't help with your mood" if not result \
            else '? '.join(
                [result['result']['setup'],result['result']['punchline']]
        )

    def handle_curious(self) -> str:
        result = self._send_request(
            'https://abhi-api.vercel.app/api/fun/facts'
        )
        return "Can't help with your mood" if not result else result['result']
