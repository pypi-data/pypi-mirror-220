"""Gulf ID and EID service websocket client."""

from .client import Client
from .exceptions import ServiceError
from .models import CardData

__all__ = [
    "Client",
    "CardData",
    "ServiceError",
]
