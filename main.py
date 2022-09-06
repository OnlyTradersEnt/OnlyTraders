import uvicorn
from fastapi import FastAPI

import settings
from content import models
from db import engine
from content.endpoints import router

app = FastAPI(title=settings.PROJECT_NAME,
              description=settings.PROJECT_DESCRIPTION,
              version=settings.PROJECT_VERSION)

models.Base.metadata.create_all(engine)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run('main:app', port=8000, debug=True, reload=True)

