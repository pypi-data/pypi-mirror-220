from typing import Optional, cast

import requests

from .types import Tag

TIMEOUT = 3
API_BASE_URI = "https://tag.rc24.xyz/api"


class RiiTagException(RuntimeError):
    """Unknown error"""


class UnauthorizedException(RiiTagException):
    """Unauthorized"""


class NotFoundException(RiiTagException):
    """Not Found"""


class RiiTag:
    def __init__(self, base_uri: str = API_BASE_URI) -> None:
        self.base_uri: str = base_uri
        self.headers: dict = {}

        self.tags: Tags = Tags(self)

    def get(self, url: str):
        return self.__request("GET", url)

    def post(self, url: str, data: Optional[dict] = None):
        if data is None:
            data = {}
        return self.__request("POST", url, data)

    def __request(self, method: str, url: str, params: Optional[dict] = None):
        if params is None:
            params = {}

        if method == "GET":
            response = requests.get(
                self.base_uri + url, params=params, headers=self.headers
            )
        elif method == "POST":
            response = requests.post(
                self.base_uri + url, json=params, headers=self.headers
            )
        else:
            raise RuntimeError("Invalid request method provided")

        if response.status_code == 401:
            raise UnauthorizedException()
        if response.status_code == 404:
            raise NotFoundException(response.json().get("error"))
        if response.status_code >= 400:
            raise RiiTagException(response.json().get("error") or "Unknown error")
        return response.json()


class Tags:
    def __init__(self, client: RiiTag):
        self.client = client

    def get(self, username: str) -> Tag:
        return cast(Tag, self.client.get(f"/user/{username}"))
