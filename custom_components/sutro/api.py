"""Sample API Client."""
import asyncio
import logging
import socket

import aiohttp
import async_timeout

TIMEOUT = 10


_LOGGER: logging.Logger = logging.getLogger(__package__)


class SutroApiClient:
    def __init__(self, token: str, session: aiohttp.ClientSession) -> None:
        """Sample API Client."""
        self._token = token
        self._session = session

    async def async_get_data(self) -> dict:
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
                }
                pool {
                    latestReading {
                        alkalinity
                        chlorine
                        ph
                        readingTime
                    }
                }
            }
        }
        """
        headers = {
            "Content-type": "application/json; charset=UTF-8",
            "Authorization": f"Bearer {self._token}",
        }
        url = "https://api.mysutro.com/graphql"
        response = await self.api_wrapper("post", url, query, headers)
        return response["data"]

    async def api_wrapper(
        self, method: str, url: str, data: dict, headers: dict
    ) -> dict:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(TIMEOUT, loop=asyncio.get_event_loop()):
                if method == "get":
                    response = await self._session.get(url, headers=headers)
                    return await response.json()

                elif method == "put":
                    await self._session.put(url, headers=headers, json=data)

                elif method == "patch":
                    await self._session.patch(url, headers=headers, json=data)

                elif method == "post":
                    await self._session.post(url, headers=headers, json=data)

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
