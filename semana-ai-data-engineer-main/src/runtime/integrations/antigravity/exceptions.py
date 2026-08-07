class RequestGatewayError(Exception):
    """Base error for failures before a valid RuntimeRequest exists."""


class InvalidRequestError(RequestGatewayError):
    """Raised when the external request cannot produce a valid RuntimeRequest."""