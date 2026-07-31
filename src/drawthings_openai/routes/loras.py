from fastapi import APIRouter

from drawthings_openai.dependencies import ImageClientDependency
from drawthings_openai.models.api_models import OpenAILora, OpenAIModelList

router = APIRouter(
    prefix="/v1",
    tags=["loras"],
)


@router.get("/loras", response_model=OpenAIModelList)
async def list_models(
    client: ImageClientDependency,
) -> OpenAIModelList:
    drawthings_loras = await client.list_loras()

    return OpenAIModelList(
        data=[
            OpenAILora(id=model["file"], name=model["name"], version=model["version"])
            for model in drawthings_loras
        ]
    )
