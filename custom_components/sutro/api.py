"""Sutro API Client."""
from __future__ import annotations

import asyncio
import json
import logging
import socket
from typing import Any

import aiohttp
import async_timeout

TIMEOUT = 10


_LOGGER: logging.Logger = logging.getLogger(__package__)

SUTRO_GRAPHSQL_URL = "https://api.mysutro.com/graphql"


class SutroApiClient:
    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Sample API Client."""
        self._session = session

    async def api_wrapper(
        self, method: str, url: str, data: Any, headers: dict
    ) -> dict | None:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(TIMEOUT):
                if method == "get":
                    response = await self._session.get(url, headers=headers)
                    return await response.json()

                if method == "post":
                    response = await self._session.post(url, headers=headers, data=data)
                    return await response.json()

                if method == "put":
                    await self._session.put(url, headers=headers, data=data)

                elif method == "patch":
                    await self._session.patch(url, headers=headers, data=data)

        except asyncio.TimeoutError as exception:
            _LOGGER.error(
                "Timeout error fetching information from %s - %s",
                url,
                exception,
            )
        except (KeyError, TypeError) as exception:
            _LOGGER.error(
                "Error parsing information from %s - %s",
                url,
                exception,
            )
        except (aiohttp.ClientError, socket.gaierror) as exception:
            _LOGGER.error(
                "Error fetching information from %s - %s",
                url,
                exception,
            )
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Something really wrong happened! - %s", exception)

        return None


class SutroLoginApiClient(SutroApiClient):
    """Sutro API Client class to handle login."""

    async def async_get_login(self, email, password) -> dict | None:
        """Login with the Sutro Credentials and get the Token."""

        query = """
            mutation ($email: String!, $password: String!){
                login(email: $email, password: $password) {
                    user {
                        firstName
                        lastName
                        email
                    }
                    token
                }
            }
            """
        payload = {
            "query": query,
            "variables": {
                "email": email,
                "password": password,
            },
        }

        headers = {
            "Content-Type": "application/json",
        }

        response = await self.api_wrapper(
            method="post",
            url=SUTRO_GRAPHSQL_URL,
            data=json.dumps(payload),
            headers=headers,
        )
        if response:
            return response["data"]
        return None


class SutroDataApiClient(SutroApiClient):
    """Sutro API Client class to get data"""

    def __init__(self, token: str, session: aiohttp.ClientSession) -> None:
        """Inititalize the Data API Class."""
        super().__init__(session)
        self._token = token

    async def async_get_data(self) -> dict | None:
        """Get data from the API."""
        query = """
        {
            me {
                id
                firstName
                device {
                    batteryLevel
                    serialNumber
                    temperature
                    cartridgeCharges
                    health
                    coreStatus
                    lidOpen
                    online
                    shouldTakeReadings
                    lastMessage
                    currentFirmwareVersion
                }
                hub {
                    online
                    chargerStatus
                    ssid
                    lastMessage
                }
                pool {
                    latestReading {
                        alkalinity
                        bromine
                        chlorine
                        ph
                        readingTime
                    }
                }
            }
        }
        """
        headers = {
            "Authorization": f"Bearer {self._token}",
        }
        response = await self.api_wrapper("post", SUTRO_GRAPHSQL_URL, query, headers)
        if response:
            return response["data"]
        return None
