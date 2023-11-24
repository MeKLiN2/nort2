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

        self.password = password
        self._proxy = proxy
        self._token = None


    def login(self):
        """
        Makes an HTTP login POST to Tinychat.
        """
        if self._token is None:
            self._parse_token()

        url = 'https://tinychat.com/login'

        form_data = {
            'login_username': self.account,
            'login_password': self.password,
            'remember': '1',
            'next': 'https://tinychat.com/',
            '_token': self._token
        }

        login_response = web.post(url=url, data=form_data, proxy=self._proxy)

        self._parse_token(response=login_response)

        return self.is_logged_in()

    def auto_login(self):
        """
        Automatically logs in without user intervention.
        """
        if not self.is_logged_in():
            self.login()
