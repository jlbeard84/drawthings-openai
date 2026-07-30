from drawthings_openai.constants import CLIENT_CONNECTION_TIMEOUT_ERROR_MESSAGE


class ApplicationError(Exception):
    """Base class for all errors"""

    pass


class ClientConnectionError(ApplicationError):
    """Errors from grpc client rethrow as this class"""

    def __init__(self, target: str, timeout_period: float) -> None:
        super().__init__(CLIENT_CONNECTION_TIMEOUT_ERROR_MESSAGE.format(target, timeout_period))

    pass
