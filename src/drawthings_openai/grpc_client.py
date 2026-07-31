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
from drawthings_openai.models.app_models import ModelCatalog
from drawthings_openai.protocols import ImageGenerationService


class ImageClient:
    def __init__(
        self,
        target: str = DEFAULT_IMAGE_SERVER_TARGET,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        is_insecure: bool = DEFAULT_INSECURE_SERVER,
    ) -> None:
        self._target = target
        self._timeout = timeout

        self._model_catalog: ModelCatalog = ModelCatalog()
        self._cache_updated_at: float | None = None

        if is_insecure:
            self._client_channel = grpc.aio.insecure_channel(target)
        else:
            raise NotImplementedError("Secure server not implemented yet")

        generated_stub = imageService_pb2_grpc.ImageGenerationServiceStub(self._client_channel)
        self._service_stub = cast(ImageGenerationService, generated_stub)

    async def list_models(self) -> list[dict[str, Any]]:
        await self._populate_model_cache()
        return list(self._model_catalog.models)

    async def list_loras(self) -> list[dict[str, Any]]:
        await self._populate_model_cache()
        return list(self._model_catalog.loras)

    async def close(self) -> None:
        await self._client_channel.close()

    async def __aenter__(self) -> ImageClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()

    async def _populate_model_cache(self) -> None:

        if (
            self._cache_updated_at is not None
            and monotonic() - self._cache_updated_at < MODEL_CACHE_TIMEOUT_SECONDS
        ):
            return

        response = await self._get_echo_response()

        if response.HasField("override"):
            self._model_catalog.models = json.loads(response.override.models)
            self._model_catalog.loras = json.loads(response.override.loras)
            self._model_catalog.control_nets = json.loads(response.override.controlNets)
            self._model_catalog.textual_inversions = json.loads(response.override.textualInversions)
            self._model_catalog.upscalers = json.loads(response.override.upscalers)
            self._cache_updated_at = monotonic()

    async def _get_echo_response(self) -> imageService_pb2.EchoReply:
        try:
            response = await self._service_stub.Echo(
                imageService_pb2.EchoRequest(name=GRPC_IDENTIFIER), timeout=self._timeout
            )

            print(response)

            return response
        except grpc.aio.AioRpcError as error:
            if error.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                raise ClientConnectionError(self._target, self._timeout) from error
            raise
