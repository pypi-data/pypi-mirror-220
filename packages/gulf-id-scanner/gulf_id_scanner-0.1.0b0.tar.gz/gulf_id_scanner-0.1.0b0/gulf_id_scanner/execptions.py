"""Exceptions raised by WS client."""


class ServiceError(Exception):
    """Base class error."""


class ConnectError(Exception):
    """Error connecting to scanner server."""


class ReadError(ServiceError):
    """Raise error if fail to read card."""


class ServiceDisconnected(ServiceError):
    """Raise error if service is disconnected."""


class ServiceUnavailable(ServiceError):
    """Raise error if no smart card service is detected."""
