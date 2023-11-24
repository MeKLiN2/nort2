# -*- coding: utf-8 -*-
from util import web
import logging
import requests
from util import Color
from util.response import Response

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
                self.console.write("Error decoding JSON: {}".format(e), Color.B_RED)
                return None

            pattern = '<link rel="manifest" href="/webrtc/'
            # Continue with the rest of your code...
            # ...

        else:
            self.console.write("Error during request. Status code: {}".format(response.status_code), Color.B_RED)
            return None

    @classmethod
    def _check_status(cls, response):
        """
        Check the status of the response. Raise an exception if the status is not ok.

        :param response: The response object.
        """
        if not response.ok:
            raise requests.RequestException(
                "HTTP error. Status code: {}".format(response.status_code))


    @classmethod
    def connect_token(cls, room, console):
        url = 'https://tinychat.com/api/v1.0/room/token/{0}'.format(room)

        try:
            response = web.get(url, as_json=True)
            cls._check_status(response)  # Check for HTTP errors
            response_json = response.json
        except requests.RequestException as e:
            cls._write_error(console, "Error during request: {}".format(e))
            cls._write_error(console, "Exception details: {}".format(e))
            return None
        except ValueError as e:
            cls._write_error(console, "Error decoding JSON: {}".format(e))
            return None

        if 'result' not in response_json:
            cls._write_error(console, "Unexpected response format. Missing 'result' key.")
            return None

        if response_json['result'] != 'success':
            cls._write_error(console, "Failed to retrieve connect token. Result: {}".format(response_json['result']))
            return None

        return {
            'token': response_json.get('result'),
            'endpoint': response_json.get('endpoint')
        }


    @classmethod
    def user_info(cls, account):
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
            self.console.write("Error during request: {}".format(e), Color.B_RED)
            return None
        except ValueError as e:
            self.console.write("Error decoding JSON: {}".format(e), Color.B_RED)
            return None

        if 'result' not in response_json:
            self.console.write("Unexpected response format. Missing 'result' key.", Color.B_RED)
            return None

        if response_json['result'] != 'success':
            self.console.write("Failed to retrieve user info. Result: {}".format(response_json['result']), Color.B_RED)
            return None

        return {
            'biography': response_json.get('biography'),
            'gender': response_json.get('gender'),
            'location': response_json.get('location'),
            'role': response_json.get('role'),
            'age': response_json.get('age')
        }





    def _write_error(self, error):
        """
        Write error information to the console using the console's write method.
        """
        self.console.write(error, color=Color.B_RED)

