from bootstrap import create_system
from gateway.app import build_gateway


def create_app():
    container = create_system()
    return build_gateway(container)


if __name__ == "__main__":
    import uvicorn

    from config import Settings

    settings = Settings()
    uvicorn.run("main:create_app", factory=True, host=settings.host, port=settings.port, reload=False)
