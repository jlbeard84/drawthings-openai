from fastapi import APIRouter

from drawthings_openai.dependencies import ImageClientDependency
from drawthings_openai.models.api_models import OpenAIModel, OpenAIModelList

router = APIRouter(
    prefix="/v1",
    tags=["models"],
)


@router.get("/models", response_model=OpenAIModelList)
async def list_models(
    client: ImageClientDependency,
) -> OpenAIModelList[OpenAIModel]:
    drawthings_models = await client.list_models()

    return OpenAIModelList(
        data=[
            OpenAIModel(id=model["file"], name=model["name"], version=model["version"])
            for model in drawthings_models
        ]
    )
