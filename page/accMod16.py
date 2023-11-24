

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
from bs4 import BeautifulSoup
from util import web
from util.web import WebSession

log = logging.getLogger(__name__)

def logger_setup():
    """
    Set up the logger for the acc module.
    """
    logging.basicConfig(level=logging.DEBUG)
    # Add any additional configuration for your logger if needed
    # ...


class Account:
    def __init__(self, account=None, password=None, proxy=None):
        self.account = account  # Add this line to initialize the account attribute
        self.password = password
        self._proxy = proxy
        self._token = None

    def _parse_token(self, response=None):
        """
        Parse the Tinychat CSRF token from the HTML response.
        """
        if response is None:
            log.error("Response object is None.")
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        
        if soup is None:
            log.error("Failed to create BeautifulSoup object.")
            return

        token_tag = soup.find('input', {'name': '_token'})
        
        if token_tag is None:
            log.error("Failed to retrieve CSRF token. Unable to log in.")
            return

        self._token = token_tag['value']


    def is_logged_in(self):
        """
        Check if logged in to Tinychat.

        :return: True if logged in, else False.
        :rtype: bool
        """
        web_session = WebSession()  # Create an instance of WebSession
        has_cookie = web_session.has_cookie('pass')
        if has_cookie:
            is_expired = web_session.is_cookie_expired('pass')
            if is_expired:
                return False
            return True
        return False

    def login(self):
        """
        Makes an HTTP login POST to Tinychat.

        :return: True if login is successful, else False.
        :rtype: bool
        """
        # Ensure the token is fetched before attempting to log in
        self._parse_token()

        if self._token is None:
            log.error("Failed to retrieve CSRF token. Unable to log in.")
            return False

        url = 'https://tinychat.com/login'

        form_data = {
            'login_username': self.account,
            'login_password': self.password,
            'remember': '1',
            'next': 'https://tinychat.com/',
            '_token': self._token
        }

        login_response = web.post(url=url, data=form_data, proxy=self._proxy)

        if login_response is None:
            log.error("Login response is None.")
            return False

        if login_response.content is None:
            log.error("Login response has no content.")
            return False

        log.debug("Login response content: %s", login_response.content)

        # Update the token after login
        self._parse_token(response=login_response)

        return self.is_logged_in()

    def auto_login(self):
        """
        Automatically logs in without user intervention.
        """
        if not self.is_logged_in():
            self.login()



    def is_logged_in(self):
        """
        Check if logged in to Tinychat.

        :return: True if logged in, else False.
        :rtype: bool
        """
        web_session = WebSession()  # Create an instance of WebSession
        has_cookie = web_session.has_cookie('pass')
        if has_cookie:
            is_expired = web_session.is_cookie_expired('pass')
            if is_expired:
                return False
            return True
        return False

    def login(self):
        """
        Makes an HTTP login POST to Tinychat.

        :return: True if login is successful, else False.
        :rtype: bool
        """
        if self._token is None:
            self._parse_token()

        if self._token is None:
            log.error("Failed to retrieve CSRF token. Unable to log in.")
            return False

        url = 'https://tinychat.com/login'

        form_data = {
            'login_username': self.account,
            'login_password': self.password,
            'remember': '1',
            'next': 'https://tinychat.com/',
            '_token': self._token
        }

        login_response = web.post(url=url, data=form_data, proxy=self._proxy)

        if login_response is None:
            log.error("Login response is None.")
            return False

        if login_response.content is None:
            log.error("Login response has no content.")
            return False

        log.debug("Login response content: %s", login_response.content)

        self._parse_token(response=login_response)

        return self.is_logged_in()


    def auto_login(self):
        """
        Automatically logs in without user intervention.
        """
        if not self.is_logged_in():
            self.login()

