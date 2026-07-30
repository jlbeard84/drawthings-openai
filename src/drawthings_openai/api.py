import asyncio

from drawthings_openai.errors import ClientConnectionError
from drawthings_openai.grpc_client import ImageClient
from drawthings_openai.settings import settings


async def main() -> None:
    try:
        async with ImageClient(
            target=settings.server_target,
            is_insecure=settings.insecure_server,
            timeout=settings.server_timeout,
        ) as client:
            models = await client.list_models()
            print(models)

            loras = await client.list_loras()
            print(loras)
    except ClientConnectionError as cce:
        print(cce)


if __name__ == "__main__":
    asyncio.run(main())
