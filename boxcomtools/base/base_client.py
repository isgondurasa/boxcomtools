# base_client.py
import json
import logging
from urllib.parse import urlencode

import aiohttp

from boxcomtools.base.exceptions import (NoClientID,
                                         NoClientSecret)


class BaseClient:
    def __init__(self, client_id, client_secret,
                 access_token=None, refresh_token=None):
        if not client_id:
            raise NoClientID

        if not client_secret:
            raise NoClientSecret

        self._client_id = client_id
        self._client_secret = client_secret
        self._access_token = access_token
        self._refresh_token = refresh_token

    @property
    def access_token(self):
        return self._access_token

    @property
    def refresh_token(self):
        return self._refresh_token

    @property
    def tokens(self):
        return self.access_token, self.refresh_token

    async def _authenticate(self, url, headers=None, data=None):
        if not data:
            data = {}

        if not headers:
            headers = self.auth_headers

        async with aiohttp.ClientSession() as session:
            async with session.post(url,
                                    headers=headers,
                                    data=data) as resp:
                body = await resp.text()
                try:
                    body = json.loads(body)
                except ValueError:
                    logging.exception("Can't parse response")
                    raise
                self._access_token = body.get('access_token')
                self._refresh_token = body.get('refresh_token')
                return self._access_token, self._refresh_token
        raise Exception("")

    @property
    def auth_headers(self):
        return {
            'content-type': 'application/x-www-form-urlencoded'
        }

    @property
    def auth_url(self):
        """
        return: auth_url
        """
        return "%s?%s" % (self.auth_endpoint, urlencode(self.url_params))

