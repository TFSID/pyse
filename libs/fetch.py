import os
import gzip
import threading
import http.cookiejar
import urllib.request
import urllib.parse
from utils.helper import random_agent, decode_bytes


class FetchRequest:
    _cookie_lock = threading.Lock()

    def __init__(self, **kwargs):
        self.debug = kwargs.get('debug') or False
        self.user_agent = kwargs.get('user_agent') or random_agent()
        self.timeout = kwargs.get('timeout') or 10
        self.cookie_file = kwargs.get('cookie_file') or 'cookies.txt'

        self.cookie_jar = http.cookiejar.LWPCookieJar(self.cookie_file)
        if os.path.exists(self.cookie_file):
            try:
                with self._cookie_lock:
                    self.cookie_jar.load(ignore_discard=True, ignore_expires=True)
            except Exception as e:
                if self.debug:
                    print(f"Error loading cookies: {e}")

    def get(self, url, headers=None):
        response = self.request(url=url, method='GET', headers=headers)

        return self.get_response(response)

    def post(self, url, headers=None, data=None):
        response = self.request(url=url, method='POST', headers=headers, data=data)

        return self.get_response(response)

    def request(self, url, **kwargs):
        method = kwargs.get('method') or 'GET'
        headers = kwargs.get('headers') or {}
        data = kwargs.get('data') or {}

        handler = urllib.request.HTTPCookieProcessor(self.cookie_jar)
        opener = urllib.request.build_opener(handler)
        request = urllib.request.Request(url=url, method=method)

        if isinstance(headers, dict):
            for k, v in headers.items():
                request.add_header(k, v)

        if not request.has_header('User-Agent') and self.user_agent:
            request.add_header('User-Agent', self.user_agent)

        if isinstance(data, dict):
            request.data = urllib.parse.urlencode(data).encode()

        try:
            response = opener.open(request, timeout=self.timeout)
            with self._cookie_lock:
                if os.path.exists(self.cookie_file):
                    try:
                        self.cookie_jar.load(ignore_discard=True, ignore_expires=True)
                    except Exception as e:
                        if self.debug:
                            print(f"Error loading cookies during save: {e}")
                self.cookie_jar.save(ignore_discard=True, ignore_expires=True)

            return response
        except Exception as err:
            print(err)

        return

    @staticmethod
    def get_response(response):
        if response:
            try:
                content_encoding = response.getheader('Content-Encoding')
                if content_encoding and content_encoding.lower() == 'gzip':
                    result, _ = decode_bytes(gzip.decompress(response.read()))
                else:
                    result, _ = decode_bytes(response.read())

                return result
            except Exception as err:
                print('_response error', err)

        return
