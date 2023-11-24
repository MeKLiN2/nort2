# -*- coding: utf-8 -*-

import logging
from bs4 import BeautifulSoup
from util import web
from util.web import WebSession

log = logging.getLogger(__name__)

class Console:
    """
    A simple console class for demonstration purposes.
    """

    def __init__(self, room=None, log_path=None, chat_logging=False, use_colors=False):
        self.room = room
        self.log_path = log_path
        self.chat_logging = chat_logging
        self.use_colors = use_colors

    def write(self, message, color=None):
        """
        Write a message to the console.

        :param message: The message to write.
        :param color: The color of the message (optional).
        """
        if color:
            log.info(message)  # You can enhance this to use colors in the console.
        else:
            log.info(message)

def logger_setup():
    """
    Set up the logger for the acc module.
    """
    logging.basicConfig(level=logging.DEBUG)
    # Add any additional configuration for your logger if needed
    # ...

class Account:
    def __init__(self, account=None, password=None, proxy=None, console=None):
        self.account = account
        self.password = password
        self._proxy = proxy
        self._token = None

        # Use the provided console instance or create a new one
        self.console = console or Console(room='your_room_name', log_path='your_log_path', chat_logging=True, use_colors=True)

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
        log.debug("CSRF Token retrieved: %s", self._token)  # Added logging statement

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
                log.debug("Login session has expired.")
                return False
            log.debug("Logged in.")
            return True
        log.debug("Not logged in.")
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
            self.console.write("Failed to retrieve CSRF token. Unable to log in.")
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
            self.console.write("Login response is None.")
            return False

        if login_response.content is None:
            self.console.write("Login response has no content.")
            return False

        self.console.write("Login response content: {}".format(login_response.content))

        if "logout" in login_response.url:
            self.console.write("Login successful. Redirected to: {}".format(login_response.url))
            # Update the token after login
            self._parse_token(response=login_response)
            return self.is_logged_in()

        self.console.write("Failed to login. Check your credentials.")
        self.console.write("Response URL: {}".format(login_response.url))
        self.console.write("Response Content: {}".format(login_response.content))

        # Update the token after login even if it failed (debugging purposes)
        self._parse_token(response=login_response)

        return False

    def auto_login(self):
        """
        Automatically logs in without user intervention.
        """
        if not self.is_logged_in():
            self.login()

if __name__ == "__main__":
    nortbot = Account()
    print("Starting Nortbot v 1.1.0.7")
    login_input = input("Login? [type yes or press enter=no] ")
    if login_input.lower() == "yes":
        nortbot.auto_login()

