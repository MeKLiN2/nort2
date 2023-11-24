# -*- coding: utf-8 -*-
from util import web
import logging
import requests
from util import Color

log = logging.getLogger(__name__)

class TinychatApi:
    def __init__(self, console):
        self.console = console

    @classmethod
    def rtc_version(cls, room):
        """
        Parse the current Tinychat RTC version.

        :param room: This could be a static room name,
        since we just need the html of any room.
        :type room: str
        :return: The current Tinychat RTC version, or None on parse failure.
        :rtype: str | None
        """
        url = 'https://tinychat.com/room/{0}'.format(room)
        response = requests.get(url)

        if response.status_code == 200:
            try:
                response_json = response.json()
            except ValueError as e:
                cls.console.write("Error decoding JSON: {}".format(e), Color.B_RED)
                return None

            pattern = '<link rel="manifest" href="/webrtc/'
            # Continue with the rest of your code...
            # ...

        else:
            cls.console.write("Error during request. Status code: {}".format(response.status_code), Color.B_RED)
            return None

    @classmethod
    def connect_token(cls, room, console):
        url = 'https://tinychat.com/api/v1.0/room/token/{0}'.format(room)

        try:
            response = web.get(url, as_json=True)
            response.raise_for_status()
            response_json = response.json()
        except Exception as e:
            console.write("Error during request: {}".format(e), Color.B_RED)
            console.write("Exception details: {}".format(e), Color.B_RED)
            return None

        return {
            'token': response_json.get('result'),
            'endpoint': response_json.get('endpoint')
        }

    @classmethod
    def user_info(cls, account, console):
        """
        Get the user information related to the account name.

        :param account: The Tinychat account name.
        :type account: str
        :return: A dictionary containing info about the user account.
        :rtype: dict | None
        """
        url = 'https://tinychat.com/api/v1.0/user/profile?username={0}&'.format(account)

        try:
            response = requests.get(url)
            response.raise_for_status()
            response_json = response.json()
        except requests.RequestException as e:
            console.write("Error during request: {}".format(e), Color.B_RED)
            return None
        except ValueError as e:
            console.write("Error decoding JSON: {}".format(e), Color.B_RED)
            return None

        if response_json['result'] == 'success':
            return {
                'biography': response_json['biography'],
                'gender': response_json['gender'],
                'location': response_json['location'],
                'role': response_json['role'],
                'age': response_json['age']
            }

        return None

