import logging.config
import random
import string
import time

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

import settings
from content import models
from content.endpoints import router
from db import engine

# logging setup
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)

# creating db engine
models.Base.metadata.create_all(engine)

# app setup
app = FastAPI(title=settings.PROJECT_NAME,
              description=settings.PROJECT_DESCRIPTION,
              version=settings.PROJECT_VERSION)

app.include_router(router)

"--------------------------------------------------- Middlewares ------------------------------------------------------"


# todo move this to a separate file

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """ log every request """
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response


# to maintain cross origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"---------------------------------------------------------------------------------------------------------------------"


@app.get("/", tags=['Landing Page'], description="Redirecting to documentation for now.")
async def index():
    return RedirectResponse("/docs")


if __name__ == "__main__":
    uvicorn.run('main:app', port=8000, debug=settings.DEBUG, reload=True)
