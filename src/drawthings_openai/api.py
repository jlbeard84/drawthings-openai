from drawthings_openai.errors import ClientConnectionError
from drawthings_openai.grpc_client import ImageClient
from drawthings_openai.settings import settings

client = ImageClient(
    target=settings.server_target,
    is_insecure=settings.insecure_server,
    timeout=settings.server_timeout,
)

if __name__ == "__main__":
    try:
        models = client.list_models()
        print(models)

        loras = client.list_loras()
        print(loras)
        client.close()
    except ClientConnectionError as cce:
        print(cce)
