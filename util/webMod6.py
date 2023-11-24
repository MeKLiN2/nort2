# -*- coding: utf-8 -*-

import time
import logging
import requests
import urlparse
from requests.utils import quote, unquote
from bs4 import BeautifulSoup


__all__ = ['quote', 'unquote',
           'WebSession', 'default_headers',
           'parse_url', 'get', 'post']

log = logging.getLogger(__name__)

# Default user agent string for all requests.
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'


def default_headers():
    """
    A default header template.

    :return: A default header dictionary.
    :rtype: dict
    """
    header = {
        'User-Agent': USER_AGENT
    }
    return header


def parse_url(url):
    """
    Parse a url in to its separate parts.

    :param url: A url to parse.
    :type url: str
    :return: Separate url parts.
    :rtype: tuple
    """
    return urlparse.urlparse(url)


class WebSession(object):
    """
    Session class for handling cookie operations.
    """
    session = None

    @classmethod
    def create(cls):
        """
        Create a new request.Session object.

        :return: A request Session object.
        :rtype: request.Session
        """
        log.debug('creating session object.')
        cls.session = requests.session()
        return cls.session

    @classmethod
    def has_cookie(cls, cookie_name):
        """
        Check a cookie by name to see if it exists.

        :param cookie_name: The name of the cookie.
        :type cookie_name: str
        :return: object request.session.cookie[cookie_name] or False if no cookie.
         """
        if cls.session is None:
            return False
        else:
            if cookie_name in cls.session.cookies:
                return cls.session.cookies[cookie_name]

            return False

    @classmethod
    def is_cookie_expired(cls, cookie_name):
        """
        Check if a cookie is expired.

        :param cookie_name: The name of the cookie to check.
        :type cookie_name: str
        :return: None if no session or no cookie by that name.
        True if expired else False
        """
        if cls.session is None:
            return None
        else:
            expires = int
            timestamp = int(time.time())

            for cookie in cls.session.cookies:
                if cookie.name == cookie_name:
                    expires = cookie.expires
                else:
                    return None

            if timestamp > expires:
                log.debug('cookie `%s` is expired.' % cookie_name)
                return True

            return False

    @classmethod
    def delete_cookie(cls, cookie_name):
        """
        Delete a cookie by name.

        :param cookie_name: The name of the cookie to delete.
        :type cookie_name: str
        :return: True if deleted else False
        :rtype: bool
        """
        if cls.session is None:
            return False
        else:
            if cookie_name in cls.session.cookies:
                log.debug('deleting cookie `%s`' % cookie_name)
                del cls.session.cookies[cookie_name]
                return True

            return False

    @classmethod
def _parse_token(cls, response=None):
    """
    Parse the token needed for the HTTP login POST.

    :param response: A Response object.
    :type response: Response
    """
    token_url = 'https://tinychat.com/start?#signin'
    if response is None:
        response = cls.get(url=token_url, referer=token_url)

    if len(response.errors) > 0:
        log.error(response.errors)
    else:
        if response.content is None:
            log.error("Response content is None.")
        else:
            soup = BeautifulSoup(response.content, 'html.parser')
            token = soup.find(attrs={'name': 'csrf-token'})
            if token is not None and 'content' in token:
                cls._token = token['content']
            else:
                log.error("Failed to find csrf-token in response content.")



class Response:
    """
    Class representing a response.
    """


    def __init__(self, text=None, content=None, errors=None):
        self.text = text
        self.content = content
        self.errors = errors if errors else []
        """
        Initialize the Response class.
        """
        self._response = None
        self._errors = []

        self._json = None
        self._content = None
        self._cookies = None
        self._headers = None
        self._status_code = None

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

    def __repr__(self):
        return '<%s errors=%s, content=%s, json=%s, ' \
               'cookies=%s, headers=%s, status_code=%s' % \
               (self.__class__.__name__, self.errors,
                self.content, self.json, self.cookies,
                self.headers, self.status_code)


def _request(method, url, **kwargs):
    """
    A wrapper for the request module.

    NOTE: For a full list of available keyword args,
    see http://docs.python-requests.org/en/master/api/#main-interface

    :param method: The request method.
    :type method: str
    :param url: The url of the request.
    :type url: str
    :param kwargs: Optional keyword args to pass on to the request module.
    :return: A Response object.
    :rtype: Response
    """
    log.debug('%s %s %s' % (method, url, kwargs))

    response = Response()

    default_header = default_headers()

    as_json = kwargs.pop('as_json', False)

    referer = kwargs.pop('referer', None)
    if referer is not None:
        default_header['Referer'] = referer

    headers = kwargs.pop('headers', None)
    if headers is not None and type(headers) is dict:
        kwargs['headers'] = default_header.update(headers)
    else:
        kwargs['headers'] = default_header

    proxy = kwargs.pop('proxy', '')
    if proxy:
        kwargs['proxies'] = {'https': 'http://' + proxy}

    # session handling
    if WebSession.session is None:
        session = WebSession.create()
    else:
        session = WebSession.session

    try:
        r = session.request(method, url, **kwargs)
        response.set_response(r, as_json)

    except (requests.ConnectionError, requests.RequestException) as re:
        response.set_error(re)

    finally:
        # return the response object
        return response


def get(url, referer=None, proxy=None, as_json=False):
    """
    Perform a HTTP GET request.

    :param url: The URL to request.
    :type url: str
    :param referer: The referer URL.
    :type referer: str | None
    :param proxy: The proxy URL.
    :type proxy: str | None
    :param as_json: Should the response be treated as JSON.
    :type as_json: bool
    :return: A Response object.
    :rtype: Response
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0'}

    if referer is not None:
        headers['Referer'] = referer

    try:
        response = requests.get(url, headers=headers, proxies={'http': proxy, 'https': proxy} if proxy else None)
        response.raise_for_status()

        if as_json:
            try:
                response_json = response.json()
                return Response(content=response_json)
            except ValueError as ve:
                return Response(errors=["Error decoding JSON: {}".format(ve)])

        return Response(text=response.text)

    except requests.RequestException as e:
        return Response(errors=["Error during request: {}".format(e)])



def post(url, **kwargs):
    """
    Make a POST request.

    :param url: The url of the POST request.
    :type url: str
    :param kwargs: Optional keywords args to pass along to the request module.
    :return: A Response object.
    :rtype: Response
    """
    return _request(method='POST', url=url, **kwargs)
