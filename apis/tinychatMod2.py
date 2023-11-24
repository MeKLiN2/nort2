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
from util import web

log = logging.getLogger(__name__)

class Color:
    B_RED = 'red'  # Adjust color as needed

class TinychatApi(object):

    def __init__(self, console):
        self.console = console

    def rtc_version(self, room):
        """
        Parse the current Tinychat RTC version.

        :param room: This could be a static room name,
        since we just need the html of any room.
        :type room: str
        :return: The current Tinychat RTC version, or None on parse failure.
        :rtype: str | None
        """
        url = 'https://tinychat.com/room/{0}'.format(room)
        response = web.get(url=url)

        try:
            response.raise_for_status()  # Raise HTTPError for bad responses
            response_json = response.json()
        except web.RequestException as e:
            self.console.write(f"Error during request: {e}", Color.B_RED)
            return None
        except ValueError as e:
            self.console.write(f"Error decoding JSON: {e}", Color.B_RED)
            return None

        pattern = '<link rel="manifest" href="/webrtc/'
        return response_json['content'].split(pattern)[1].split('/manifest.json">')[0]

    def connect_token(self, room):
        """
        Get the connect token and the WSS server endpoint.

        :param room: The room to get the details for.
        :type room: str
        :return: The token and the WSS endpoint.
        :rtype: dict | None
        """
        url = 'https://tinychat.com/api/v1.0/room/token/{0}'.format(room)

        try:
            response = web.get(url, as_json=True)
            response.raise_for_status()
            response_json = response.json()
        except web.RequestException as e:
            self.console.write(f"Error during request: {e}", Color.B_RED)
            return None
        except ValueError as e:
            self.console.write(f"Error decoding JSON: {e}", Color.B_RED)
            return None

        return {
            'token': response_json['result'],
            'endpoint': response_json['endpoint']
        }

    def user_info(self, account):
        """
        Get the user information related to the account name.

        :param account: The Tinychat account name.
        :type account: str
        :return: A dictionary containing info about the user account.
        :rtype: dict | None
        """
        url = 'https://tinychat.com/api/v1.0/user/profile?username={0}&'.format(account)

        try:
            response = web.get(url, as_json=True)
            response.raise_for_status()
            response_json = response.json()
        except web.RequestException as e:
            self.console.write(f"Error during request: {e}", Color.B_RED)
            return None
        except ValueError as e:
            self.console.write(f"Error decoding JSON: {e}", Color.B_RED)
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

