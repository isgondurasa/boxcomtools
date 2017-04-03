# base_object.py
import json
import logging

from collections.abc import MutableMapping
from urllib.parse import urljoin

import aiohttp


class BaseObject:

    __resource__ = ""

    def __init__(self, session=None, object_id=None):
        self._session = session
        self._object_id = object_id
        self._data = None

    def to_json(self):
        return {}

    def get_url(self, ext=None):
        """
        returns base url for resource API endpoint
        __resource__ should be defined in child classes
        """
        if not ext:
            return urljoin(self.request_url, self.__resource__, self._object_id)
        return urljoin(self.request_url, self.__resource__, self._object_id) + '/%s' % ext

    @property
    def headers(self):
        return {
            "Authorization": "Bearer " + self._session.access_token,
            "Content-Type": "application/json"
        }

    async def create(self, data=None):
        raise NotImplementedError

    async def get(self):
        """
        Returns a dict
        """
        self._data = await self.request(self.get_url())
        return self._data

    async def delete(self, object_id):
        raise NotImplementedError

    async def update(self, object_id, payload=None):
        raise NotImplementedError

    async def __request(self, url, method, headers, data):
        if isinstance(data, MutableMapping):
            data = json.dumps(data)
    
        async with method(url,
                          headers=headers,
                          data=data) as resp:
            body = await resp.text()
            try:
                return json.loads(body)
            except ValueError:
                logging.exception("Can't parse Response")

    async def request(self, url, method="GET", data=None):
        if not data: data = {}
        async with aiohttp.ClientSession() as session:
            method = getattr(session, method.lower(), None)
            if method:
                return await self.__request(url, method, self.headers, data)
            raise Exception("ERROR in object request method")


    def _attach_to_object(self, data):
        for k, v in data.items():
            try:
                setattr(self, k, v)
            except AttributeError as e:
                logging.exception(e)

    @property
    def id(self):
        return self._object_id
