import os

from fastapi import FastAPI, HTTPException, APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse
from canals import load_pipelines

from windrow import __version__
from windrow.config import ROOT_PATH, DEFAULT_PIPELINES


APP = None
PIPELINES = None


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)


def get_app() -> FastAPI:
    global APP  # pylint: disable=global-statement
    if APP:
        return APP

    APP = FastAPI(title="Windrow - Haystack REST API", debug=True, version=__version__, root_path=ROOT_PATH)

    from windrow.routers import pipelines

    router = APIRouter()
    router.include_router(pipelines.router, tags=["pipelines"])
    APP.add_exception_handler(HTTPException, http_error_handler)
    APP.include_router(router)

    return APP


def get_pipelines():
    global PIPELINES  # pylint: disable=global-statement
    if PIPELINES:
        return PIPELINES
    pipelines_path = os.environ.get("WINDROW_PIPELINES_PATH", DEFAULT_PIPELINES)
    PIPELINES = load_pipelines(pipelines_path)
    return PIPELINES
