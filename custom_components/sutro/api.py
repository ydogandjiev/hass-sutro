"""Sutro API Client."""
from __future__ import annotations

import asyncio
import json
import logging
import socket
from datetime import datetime
from datetime import timezone
from typing import Any

import aiohttp
import async_timeout

# Set a timeout of 10 seconds for API requests
TIMEOUT = 10

# Initialize a logger for logging errors and debugging
_LOGGER = logging.getLogger(__package__)

# URL for the Sutro GraphQL API
SUTRO_GRAPHSQL_URL = "https://api.mysutro.com/graphql"


class SutroApiClient:
    """Base API Client for making requests to the Sutro API."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Initialize the API Client."""
        self._session = session

    async def api_wrapper(
        self, method: str, url: str, data: Any, headers: dict
    ) -> dict | None:
        """Wrap the API requests to handle errors and exceptions."""
        try:
            async with async_timeout.timeout(TIMEOUT):
                if method == "get":
                    response = await self._session.get(url, headers=headers)
                elif method == "post":
                    response = await self._session.post(url, headers=headers, data=data)
                elif method == "put":
                    response = await self._session.put(url, headers=headers, data=data)
                elif method == "patch":
                    response = await self._session.patch(
                        url, headers=headers, data=data
                    )
                else:
                    raise ValueError("Invalid method specified")

                response.raise_for_status()
                return await response.json()
        except asyncio.TimeoutError as exception:
            _LOGGER.error(
                "Timeout error fetching information from %s - %s", url, exception
            )
        except aiohttp.ClientError as exception:
            _LOGGER.error("Error fetching information from %s - %s", url, exception)
        except (KeyError, TypeError, ValueError) as exception:
            _LOGGER.error("Error parsing information from %s - %s", url, exception)
        except socket.gaierror as exception:
            _LOGGER.error("Error resolving the hostname - %s", exception)
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
                        pool {
                            type
                        }
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
    """Sutro API Client class to get data."""

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
                    latestRecommendations {
                        conflictWarning
                        recommendations {
                            id
                            chemical {
                                behaviour
                                image
                                name
                                types
                                packageSize
                                packageSizeUnit
                                upc
                            }
                            completedAt
                            expiredAt
                            type
                            decision
                            explanation
                            treatment
                        }
                    }
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
        payload = {
            "query": query,
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._token}",
        }
        response = await self.api_wrapper(
            "post", SUTRO_GRAPHSQL_URL, json.dumps(payload), headers
        )
        if response:
            return response["data"]
        return None

    async def async_complete_recommendation(self, recommendation_id) -> dict | None:
        """Complete a recommendation."""
        query = """
        mutation ($recommendationId: ID!, $completedAt: DateTime) {
            completeRecommendation(recommendationId: $recommendationId, completedAt: $completedAt) {
                completedAt
                success
            }
        }
        """
        current_time = datetime.now(timezone.utc).isoformat()

        payload = {
            "query": query,
            "variables": {
                "recommendationId": recommendation_id,
                "completedAt": current_time,
            },
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._token}",
        }
        response = await self.api_wrapper(
            "post", SUTRO_GRAPHSQL_URL, json.dumps(payload), headers
        )
        if response:
            return response["data"]
        return None

    async def async_uncomplete_recommendation(self, recommendation_id) -> dict | None:
        """Uncomplete a recommendation."""
        query = """
        mutation ($recommendationId: ID!, $completedAt: DateTime) {
            completeRecommendation(recommendationId: $recommendationId, completedAt: $completedAt) {
                completedAt
                success
            }
        }
        """
        payload = {
            "query": query,
            "variables": {
                "recommendationId": recommendation_id,
                "completedAt": None,
            },
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._token}",
        }

        response = await self.api_wrapper(
            "post", SUTRO_GRAPHSQL_URL, json.dumps(payload), headers
        )
        if response:
            return response["data"]
        return None
