# util/response.py
import logging
import requests
from util import Color

log = logging.getLogger(__name__)

class CustomHTTPError(Exception):
    pass

class Response(requests.Response):
    """
    Class representing a response.
    """
    def __init__(self, console):
        """
        Initialize the Response class.

        :param console: The console object with a write method.
        """
        super(Response, self).__init__()

        self._response = None
        self._errors = []

        self._json = None
        self._content = None
        self._cookies = None
        self._headers = None
        self._status_code = None

        # Console object with a write method
        self._console = console

    def check_status(self):
        """
        Check the status code and raise an exception if it's an error.
        """
        if hasattr(self._response, 'status_code') and 400 <= self._response.status_code < 600:
            raise CustomHTTPError("HTTP error. Status code: {}".format(self._response.status_code))

    def raise_for_status(self):
        """
        Raise an HTTPError if the HTTP request returned an unsuccessful status code.
        """
        if hasattr(self._response, 'status_code') and 400 <= self._response.status_code < 600:
            raise requests.HTTPError("HTTP error. Status code: {}".format(self._response.status_code))

    def set_error(self, error):
        """
        Set response error.

        :param error: Error description.
        """
        self._errors.append(error)

    def set_response(self, response, as_json=False):
        """
        Set the response of a request.

        :param response: A request response object.
        :param as_json: Is the response expected to be json.
        :type as_json: bool
        """
        if as_json:
            try:
                self._json = response.json()
            except ValueError as ve:
                self.set_error(ve)

        self._response = response

        # Check for HTTP errors
        if hasattr(response, 'status_code') and 400 <= response.status_code < 600:
            log.error("HTTP error. Status code: {}".format(response.status_code))
            self.set_error("HTTP error. Status code: {}".format(response.status_code))

        self.console_write()

    @property
    def errors(self):
        """
        A list of request errors.

        :return: A list of errors related to a request.
        :rtype: list
        """
        return self._errors

    @property
    def content(self):
        """
        The content(text) of a request.

        :return: The content of a request.
        :rtype: str
        """
        return self._response.text

    @property
    def json(self):
        """
        A response as json.

        :return: Response as json
        """
        return self._json

    @property
    def cookies(self):
        """
        Cookies of this request.

        :return: Cookies for this request.
        """
        return self._response.cookies

    @property
    def headers(self):
        """
        Headers of this request.

        :return: Header related to this request.
        """
        return self._response.headers

    @property
    def status_code(self):
        """
        Status code of the request.

        :return: The status code of this request.
        """
        return self._response.status_code

    def console_write(self):
        """
        Write information to the console using the console's write method.
        """
        log.info('Response successfully processed.')
        log.info("Status Code: {}".format(self.status_code))
        log.info("Response Content: {}".format(self.content))
        log.info("Response JSON: {}".format(self.json))
        log.info("Response Cookies: {}".format(self.cookies))
        log.info("Response Headers: {}".format(self.headers))
        log.info("Errors: {}".format(self.errors))

        # Using the console's write method
        self._console.write("Status Code: {}".format(self.status_code), color=Color.RED, ts=False)
        self._console.write("Response Content: {}".format(self.content), color=Color.RED, ts=False)
        self._console.write("Response JSON: {}".format(self.json), color=Color.RED, ts=False)
        self._console.write("Response Cookies: {}".format(self.cookies), color=Color.RED, ts=False)
        self._console.write("Response Headers: {}".format(self.headers), color=Color.RED, ts=False)
        self._console.write("Errors: {}".format(self.errors), color=Color.RED, ts=False)

