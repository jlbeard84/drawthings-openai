import json

import pytest

from drawthings_openai.generated import imageService_pb2


@pytest.fixture
def echo_response() -> imageService_pb2.EchoReply:
    return imageService_pb2.EchoReply(
        override=imageService_pb2.MetadataOverride(
            models=json.dumps(
                [
                    {
                        "file": "test-model.ckpt",
                        "name": "Test Model",
                        "version": "test",
                    }
                ]
            ).encode(),
            loras=b"[]",
            controlNets=b"[]",
            textualInversions=b"[]",
            upscalers=b"[]",
        )
    )
