import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware

import settings
from content import models
from db import engine
from content.endpoints import router

app = FastAPI(title=settings.PROJECT_NAME,
              description=settings.PROJECT_DESCRIPTION,
              version=settings.PROJECT_VERSION)

models.Base.metadata.create_all(engine)

app.include_router(router)

# to maintain cross origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=['Landing Page'], description="Redirecting to documentation for now.")
async def index():
    return RedirectResponse("/docs")


if __name__ == "__main__":
    uvicorn.run('main:app', port=8000, debug=settings.DEBUG, reload=True)

