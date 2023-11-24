# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2019 Nortxort

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import logging
import requests
from util import Color
from util import web

log = logging.getLogger(__name__)

class TinychatApi:
    @classmethod
    def rtc_version(cls, room, console):
        """
        Parse the current Tinychat RTC version.

        :param room: This could be a static room name,
        since we just need the html of any room.
        :type room: str
        :param console: Console instance for writing messages.
        :type console: YourConsoleClass
        :return: The current Tinychat RTC version, or None on parse failure.
        :rtype: str | None
        """
        url = 'https://tinychat.com/room/{0}'.format(room)
        response = requests.get(url)

        try:
            response.raise_for_status()
            response_json = response.json()
        except requests.RequestException as e:
            if response.status_code == 500:
                console.write("Error 500: Internal Server Error", Color.B_RED)
            else:
                console.write("Error during request: {}".format(e), Color.B_RED)
            return None
        except ValueError as e:
            console.write("Error decoding JSON: {}".format(e), Color.B_RED)
            return None

        pattern = '<link rel="manifest" href="/webrtc/'

    @classmethod
    def connect_token(cls, room, console):
        """
        Get the connect token and the WSS server endpoint.

        :param room: The room to get the details for.
        :type room: str
        :param console: The console instance.
        :type console: YourConsoleClass
        :return: The token and the WSS endpoint.
        :rtype: dict | None
        """
        url = 'https://tinychat.com/api/v1.0/room/token/{0}'.format(room)

        try:
            response = web.get(url, as_json=True)
            response.raise_for_status()
            response_json = response.json()
        except Exception as e:
            console.write("Error during request: {}".format(e), Color.B_RED)
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
        :param console: Console instance for writing messages.
        :type console: YourConsoleClass
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

