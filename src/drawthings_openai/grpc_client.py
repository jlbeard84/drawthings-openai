import json
from datetime import datetime, timedelta
from typing import Any, cast

import grpc

from drawthings_openai.constants import (
    DEFAULT_IMAGE_SERVER_TARGET,
    DEFAULT_INSECURE_SERVER,
    DEFAULT_TIMEOUT_SECONDS,
    GRPC_IDENTIFIER,
    MODEL_CACHE_TIMEOUT_MINUTES,
)
from drawthings_openai.errors import ClientConnectionError
from drawthings_openai.generated import imageService_pb2, imageService_pb2_grpc
from drawthings_openai.protocols import ImageGenerationService


class ImageClient:
    def __init__(
        self,
        target: str = DEFAULT_IMAGE_SERVER_TARGET,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        is_insecure: bool = DEFAULT_INSECURE_SERVER,
    ) -> None:
        self._timeout = timeout

        self._cached_models_time: datetime | None = None
        self._cached_models: list[dict[str, Any]] = []
        self._cached_loras: list[dict[str, Any]] = []
        self._cached_control_nets: list[dict[str, Any]] = []
        self._cached_textual_inversions: list[dict[str, Any]] = []
        self._cached_upscalers: list[dict[str, Any]] = []

        if is_insecure:
            self._client_channel = grpc.insecure_channel(target)
        else:
            raise NotImplementedError("Secure server not implemented yet")

        try:
            grpc.channel_ready_future(self._client_channel).result(timeout=self._timeout)
        except grpc.FutureTimeoutError:
            self._client_channel.close()
            raise ClientConnectionError(target, self._timeout) from None

        generated_stub = imageService_pb2_grpc.ImageGenerationServiceStub(self._client_channel)
        self._service_stub = cast(ImageGenerationService, generated_stub)

    def list_models(self) -> list[dict[str, Any]]:
        self._populate_model_cache()
        return self._cached_models

    def list_loras(self) -> list[dict[str, Any]]:
        self._populate_model_cache()
        return self._cached_loras

    def close(self) -> None:
        self._client_channel.close()

    def __enter__(self) -> ImageClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def _populate_model_cache(self) -> None:

        check_time = datetime.now()

        if (
            self._cached_models_time is not None
            and check_time - self._cached_models_time
            < timedelta(minutes=MODEL_CACHE_TIMEOUT_MINUTES)
        ):
            return

        response = self._get_echo_response()

        if response.HasField("override"):
            self._cached_models = json.loads(response.override.models)
            self._cached_loras = json.loads(response.override.loras)
            self._cached_control_nets = json.loads(response.override.controlNets)
            self._cached_textual_inversions = json.loads(response.override.textualInversions)
            self._cached_upscalers = json.loads(response.override.upscalers)
            self._cached_models_time = datetime.now()

    def _get_echo_response(self) -> imageService_pb2.EchoReply:
        response = self._service_stub.Echo(
            imageService_pb2.EchoRequest(name=GRPC_IDENTIFIER), timeout=self._timeout
        )

        return response
