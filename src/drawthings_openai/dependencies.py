from typing import Annotated, cast

from fastapi import Depends, Request

from drawthings_openai.grpc_client import ImageClient


def get_image_client(request: Request) -> ImageClient:
    return cast(ImageClient, request.app.state.image_client)


ImageClientDependency = Annotated[ImageClient, Depends(get_image_client)]
