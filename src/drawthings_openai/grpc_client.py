import json
from time import monotonic
from typing import Any, cast

import grpc

from drawthings_openai.constants import (
    DEFAULT_IMAGE_SERVER_TARGET,
    DEFAULT_INSECURE_SERVER,
    DEFAULT_TIMEOUT_SECONDS,
    GRPC_IDENTIFIER,
    MODEL_CACHE_TIMEOUT_SECONDS,
)
from drawthings_openai.errors import ClientConnectionError
from drawthings_openai.generated import imageService_pb2, imageService_pb2_grpc
from drawthings_openai.models import ModelCatalog
from drawthings_openai.protocols import ImageGenerationService


class ImageClient:
    def __init__(
        self,
        target: str = DEFAULT_IMAGE_SERVER_TARGET,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        is_insecure: bool = DEFAULT_INSECURE_SERVER,
    ) -> None:
        self._timeout = timeout

        self._model_catalog: ModelCatalog = ModelCatalog()
        self._cache_updated_at: float | None = None

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
        return list(self._model_catalog.models)

    def list_loras(self) -> list[dict[str, Any]]:
        self._populate_model_cache()
        return list(self._model_catalog.loras)

    def close(self) -> None:
        self._client_channel.close()

    def __enter__(self) -> ImageClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def _populate_model_cache(self) -> None:

        if (
            self._cache_updated_at is not None
            and monotonic() - self._cache_updated_at < MODEL_CACHE_TIMEOUT_SECONDS
        ):
            return

        response = self._get_echo_response()

        if response.HasField("override"):
            self._model_catalog.models = json.loads(response.override.models)
            self._model_catalog.loras = json.loads(response.override.loras)
            self._model_catalog.control_nets = json.loads(response.override.controlNets)
            self._model_catalog.textual_inversions = json.loads(response.override.textualInversions)
            self._model_catalog.upscalers = json.loads(response.override.upscalers)
            self._cache_updated_at = monotonic()

    def _get_echo_response(self) -> imageService_pb2.EchoReply:
        response = self._service_stub.Echo(
            imageService_pb2.EchoRequest(name=GRPC_IDENTIFIER), timeout=self._timeout
        )

        return response
