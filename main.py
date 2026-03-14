from fastapi import FastAPI

from app.domains.post.adapter.inbound.api.post_router import router as post_router
from app.infrastructure.config import get_settings

settings = get_settings()

app = FastAPI()

app.include_router(post_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=33333)
