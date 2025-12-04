import os
import gzip
import random
import hashlib
import http.cookiejar
import urllib.request
import urllib.parse
from utils.helper import split_url, dir_exist, file_exist, random_agent, decode_bytes


class FetchRequest:
    def __init__(self, **kwargs):
        self.debug = kwargs.get('debug') or False
        self.user_agent = kwargs.get('user_agent') or random_agent()
        self.timeout = kwargs.get('timeout') or 10
        self.cookie_dir = kwargs.get('cookie_dir') or 'cookie'
        self.cookie_ext = kwargs.get('cookie_ext') or '_cookie'
        self.cookie_file = None
        self.cookie = None

    def set_cookie_file(self, url):
        cookieStr = self.cookie_file

        spliturl = split_url(url)
        if spliturl.get('url'):
            cookieStr = '%s%s' % (spliturl.get('scheme'), spliturl.get('domain'))

        cookieName = hashlib.md5(cookieStr.encode()).hexdigest()
        cookieFile = '%s%s' % (cookieName, self.cookie_ext)

        if file_exist(self.cookie_dir):
            os.remove(self.cookie_dir)

        if not dir_exist(self.cookie_dir):
            os.mkdir(self.cookie_dir)

        self.cookie_file = os.path.join(self.cookie_dir, cookieFile)

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

        self.set_cookie_file(url)

        # https://developpaper.com/python-cookie-read-and-save-method/
        if file_exist(self.cookie_file):
            cookie = http.cookiejar.MozillaCookieJar()
            cookie.load(self.cookie_file, ignore_discard=True, ignore_expires=True)
        else:
            cookie = http.cookiejar.MozillaCookieJar(self.cookie_file)

        handler = urllib.request.HTTPCookieProcessor(cookie)
        opener = urllib.request.build_opener(handler)
        request = urllib.request.Request(url=url, method=method)

        if not headers:
            headers = {}
        else:
            headers = headers.copy()

        # Case-insensitive check for User-Agent
        has_user_agent = any(k.lower() == 'user-agent' for k in headers)
        if self.user_agent and not has_user_agent:
            headers['User-Agent'] = self.user_agent

        headers = self.add_fake_headers(headers)
        headers = self.shuffle_headers(headers)

        if isinstance(headers, dict):
            for k, v in headers.items():
                request.add_header(k, v)

        if isinstance(data, dict):
            request.data = urllib.parse.urlencode(data).encode()

        try:
            response = opener.open(request, timeout=self.timeout)
            cookie.save(self.cookie_file, ignore_discard=True, ignore_expires=True)

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

    @staticmethod
    def shuffle_headers(headers):
        if not isinstance(headers, dict):
            return headers

        keys = list(headers.keys())
        random.shuffle(keys)
        return {k: headers[k] for k in keys}

    @staticmethod
    def add_fake_headers(headers):
        fake_headers = {
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        # Select a random subset of fake headers to add (1 to 3 headers)
        num_fake = random.randint(1, 3)
        headers_to_add = random.sample(list(fake_headers.keys()), min(num_fake, len(fake_headers)))

        lower_keys = {k.lower() for k in headers.keys()}

        for key in headers_to_add:
            if key.lower() not in lower_keys:
                headers[key] = fake_headers[key]

        return headers
