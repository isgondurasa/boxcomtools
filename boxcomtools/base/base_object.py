# base_object.py
import json
import logging
import aiohttp


class BaseObject:
    def __init__(self, session=None, object_id=None):
        self._session = session
        self._object_id = object_id

    def get_url(self):
        raise NotImplementedError

    @property
    def headers(self):
        return {
            "Authorization": "Bearer " + self._session.access_token,
            "Content-Type": "application/json"
        }
    
    async def create(self, data=None):
        raise NotImplementedError

    async def get(self, object_id):
        raise NotImplementedError

    async def list(self):
        raise NotImplementedError

    async def delete(self, object_id):
        raise NotImplementedError

    async def update(self, object_id, payload=None):
        raise NotImplementedError


    async def __request(self, url, method, headers, data):
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
        logging.info("before request")
        
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
