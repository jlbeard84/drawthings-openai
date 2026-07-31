from typing import Literal

from pydantic import BaseModel


class OpenAIModel(BaseModel):
    id: str
    name: str
    version: str
    object: Literal["model"] = "model"
    created: int = 0
    owned_by: str = "drawthings"


class OpenAILora(BaseModel):
    id: str
    name: str
    version: str
    object: Literal["lora"] = "lora"
    created: int = 0
    owned_by: str = "drawthings"


class OpenAIModelList[T: OpenAIModel | OpenAILora](BaseModel):
    object: Literal["list"] = "list"
    data: list[T]
