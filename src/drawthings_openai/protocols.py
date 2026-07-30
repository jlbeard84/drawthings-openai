from typing import Protocol

from drawthings_openai.generated import imageService_pb2


class ImageGenerationService(Protocol):
    def Echo(
        self,
        request: imageService_pb2.EchoRequest,
        timeout: float | None = None,
    ) -> imageService_pb2.EchoReply: ...
