"""Websocket client for Emirates ID."""

from dataclasses import asdict
import logging
from enum import Enum
from typing import Any

import httpx

from gulf_id_scanner.execptions import ConnectError, RequestError
from .models import EIDContext, EIDRequest, EstablishContext, PublicData

_LOGGER = logging.getLogger(__name__)


class GulfIDClient:
    """Class for reading Gulf ID data over http."""

    def __init__(
        self,
        *,
        session: httpx.AsyncClient | None = None,
        host: str,
        port: int = 5050,
        use_ssl: bool = False,
    ) -> None:
        """Initiate class."""
        self.url = f"http://{host}:{port}/api/operation/ReadCard"
        self.session: httpx.AsyncClient = session or httpx.AsyncClient(verify=False)

    async def _async_request(
        self,
    ) -> dict[str, Any]:
        """Send a http request and return the response."""
        _LOGGER.info(
            "Sending request to %s",
            self.url,
        )
        params = {
            "ReadCardInfo": True,
            "ReadPersonalInfo": True,
            "ReadAddressDetails": True,
            "ReadBiometrics": True,
            "ReadEmploymentInfo": True,
            "ReadImmigrationDetails": True,
            "ReadTrafficDetails": True,
            "SilentReading": False,
            "ReaderIndex": -1,
            "ReaderName": "",
            "OutputFormat": "JSON",
            "ValidateCard": False,
        }
        try:
            response = await self.session.request(
                "POST", self.url, params=params, json=params
            )
        except (httpx.ConnectError, httpx.ReadTimeout) as err:
            raise ConnectError(
                f"Connection failed while sending request: {err}"
            ) from err
        _LOGGER.debug(
            "status_code: %s, response: %s", response.status_code, response.text
        )
        if response.status_code != httpx.codes.OK:
            raise RequestError(response.json()["message"])
        return response.json()

    async def read_card_data(self) -> PublicData:
        """Read data from card."""
        if self._state != WebsocketState.READY:
            await self._connect_reader()
        response = await self.send_request(self.request.read_card_data())
        card_data: PublicData = PublicData.from_xml(response["toolkit_response"])
        return card_data
