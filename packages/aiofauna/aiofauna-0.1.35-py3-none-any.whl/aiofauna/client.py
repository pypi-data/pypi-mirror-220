import base64
import functools
import io
import json
import logging
import os
from dataclasses import dataclass, field
from re import T
from typing import Any, AsyncGenerator, Dict, List, Literal, Optional, Union

from aiohttp import (ClientConnectionError, ClientConnectorSSLError,
                     ClientResponse, ClientSession, ClientTimeout,
                     TCPConnector)
from aiohttp.web_exceptions import HTTPException
from dotenv import load_dotenv
from multidict import CIMultiDict
from pydantic import BaseModel

from .errors import FaunaException
from .json import FaunaJSONEncoder, to_json
from .logging import setup_logging
from .objects import Expr
from .typedefs import LazyProxy

load_dotenv()

logging_factory = functools.partial(setup_logging, __name__)

Method = Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
Json = Union[Dict[str, Any], List[Dict[str, Any]]]
MaybeJson = Optional[Json]
Headers = Dict[str, str]
MaybeHeaders = Optional[Headers]

# Load environment variables once at the start of the program
FAUNA_SECRET = os.environ["FAUNA_SECRET"]
HEADERS = {
    "Authorization": f"Bearer {FAUNA_SECRET}",
    "Content-type": "application/json",
    "Accept": "application/json"
}


@dataclass(init=True, repr=True, unsafe_hash=False, frozen=False)
class FaunaClient(LazyProxy[ClientSession]):
    secret: str = field(default=FAUNA_SECRET)
    logger:logging.Logger = field(default_factory=logging_factory)
    session: Optional[ClientSession] = field(default=None)
        
    def __load__(self) -> ClientSession:
        if self.session is None:
            return ClientSession(
                "https://db.fauna.com",
                headers=CIMultiDict(HEADERS),
                response_class=ClientResponse,
                connector=TCPConnector(ssl=False, limit=1000,
                keepalive_timeout=10),
                timeout=ClientTimeout(total=10),
                connector_owner=True,
                trust_env=True,
                read_bufsize=2**18,
            )
        else:
            return self.session
    
    async def query(self, expr: Expr,session: Optional[ClientSession]=None) -> Any:
        if session is None:
            session = self.__load__()
        async with session as session:
            async with session.post(
                "/",
                data=to_json(expr),
            ) as response:
                try:
                    data = await response.json()
                    self.logger.info(data)
                    if data.get("resource") is not None:
                        return data["resource"]
                    if data.get("error") is not None:
                        return data["error"]
                    return data

                except (
                        FaunaException,
                        ValueError,
                        KeyError,
                        TypeError,
                        Exception,
                        UnicodeError,
                        json.JSONDecodeError,
                        RuntimeError,
                        ClientConnectionError,
                        ClientConnectorSSLError
                ) as exc:  # pylint:disable=all
                    self.logger.error(exc)
                    return {"errors": exc}
                finally:
                    await session.close()
    
    
    async def stream(self, expr: Expr) -> AsyncGenerator[str, None]:
        async with self.__load__() as session:
            async with session.post(
                "",
                data=to_json(expr),
                headers={
                    "Authorization": f"Bearer {self.secret}",
                    "Content-type": "application/json",
                    "Accept": "text/event-stream",
                    "Keep-Alive": "timeout=5, max=900",
                    "Connection": "keep-alive",
                    "Cache-Control": "no-cache",
                    "X-Last-Seen-Txn": "0",
                    "X-Request-By": "aiofauna",
                    "X-Query-By": "@obahamonde",
                },
            ) as response:
                async for chunk in response.content.iter_any():
                    try:
                        yield chunk.decode()
                    except (
                        HTTPException,
                        FaunaException,
                        ValueError,
                        KeyError,
                        TypeError,
                        Exception,
                        UnicodeError,
                        json.JSONDecodeError,
                        RuntimeError,
                        ClientConnectionError,
                        ClientConnectorSSLError
                    ) as exc:
                        self.logger.error(exc)
                        yield json.dumps({"errors": exc})


@dataclass(init=True, repr=True, unsafe_hash=False, frozen=False)
class ApiClient(LazyProxy[ClientSession]):
    """
    Generic HTTP Client
    """
    base_url: Optional[str] = field(default=None)
    headers: Optional[Headers] = field(default=None)
    limit: int = field(default=1000)
    _session: Optional[ClientSession] = field(default=None)
    
    def __post_init__(self):
        self.logger = setup_logging(self.__class__.__name__)
        if not ApiClient._session:
            ApiClient._session = self.__load__()                
    
    
    def __load__(self) -> ClientSession:
            if self.base_url and self.headers:
                return ClientSession(
                    self.base_url,
                    headers=CIMultiDict(self.headers),
                    response_class=ClientResponse,
                    connector=TCPConnector(ssl=False, limit=self.limit,
                    keepalive_timeout=10),
                    timeout=ClientTimeout(total=10),
                    connector_owner=True,
                    trust_env=True,
                    read_bufsize=2**16,
                )
            elif self.base_url:
                return ClientSession(
                    self.base_url,
                    response_class=ClientResponse,
                    connector=TCPConnector(ssl=False, limit=self.limit,
                    keepalive_timeout=10),
                    timeout=ClientTimeout(total=10),
                    connector_owner=True,
                    trust_env=True,
                    read_bufsize=2**16,
                )
            elif self.headers:
                return ClientSession(
                    headers=CIMultiDict(self.headers),
                    response_class=ClientResponse,
                    connector=TCPConnector(ssl=False, limit=self.limit,
                    keepalive_timeout=10),
                    timeout=ClientTimeout(total=10),
                    connector_owner=True,
                    trust_env=True,
                    read_bufsize=2**16,
                )
            else:
                return ClientSession(
                    response_class=ClientResponse,
                    connector=TCPConnector(ssl=False, limit=self.limit,
                    keepalive_timeout=10),
                    timeout=ClientTimeout(total=10),
                    connector_owner=True,
                    trust_env=True,
                    read_bufsize=2**16,
                )
            

    async def fetch(
        self,
        url: str,
        method: Method = "GET",
        headers: MaybeHeaders = None,
        json: MaybeJson = None):
        if self.base_url is not None:
            url = self.base_url + url
        if self.headers is not None and headers is not None:
            headers = {**self.headers, **headers}
        elif self.headers is not None:
            headers = self.headers
        async with self.__load__() as session:
            async with session.request(
                method, url, headers=headers, json=json, timeout=30
            ) as response:
                try:
                    data = await response.json()
                    return data
                except (
                    HTTPException,
                    FaunaException,
                    ValueError,
                    KeyError,
                    TypeError,
                    Exception,
                ) as exc:  # pylint:disable=broad-exception-caught, unused-variable
                    print(exc)
                    return None

    async def text(
        self,
        url: str,
        method: Method = "GET",
        headers: MaybeHeaders = None,
        json: MaybeJson = None,
    ):
        if self.base_url is not None:
            url = self.base_url + url
        if self.headers is not None and headers is not None:
            headers = {**self.headers, **headers}
        elif self.headers is not None:
            headers = self.headers
        async with self.__load__() as session:
            async with session.request(
                method, url, headers=headers, json=json, timeout=30
            ) as response:
                try:
                    data = await response.text()
                    return data
                except (
                    HTTPException,
                    FaunaException,
                    ValueError,
                    KeyError,
                    TypeError,
                    Exception,
                ) as exc:  # pylint:disable=broad-exception-caught, unused-variable
                    print(exc)
                    return None  # type: ignore

    async def stream(
        self,
        url: str,
        method: Method = "GET",
        headers: MaybeHeaders = None,
        json: MaybeJson = None,
    ):
        if self.base_url is not None:
            url = self.base_url + url
        if self.headers is not None and headers is not None:
            headers = {**self.headers, **headers}
        elif self.headers is not None:
            headers = self.headers
        async with self.__load__() as session:
            async with session.request(
                method, url, headers=headers, json=json, timeout=30
            ) as response:
                async for chunk in response.content.iter_any():
                    try:
                        yield chunk.decode()
                    except (
                        HTTPException,
                        FaunaException,
                        ValueError,
                        KeyError,
                        TypeError,
                        Exception,
                    ) as exc:
                        print(exc)