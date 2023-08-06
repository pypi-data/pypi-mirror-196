from typing import Dict, Any

import logging
import time
import json

from fastapi import FastAPI, APIRouter

from windrow import __version__ as windrow_version

# from haystack import __version__ as haystack_version
from canals import Pipeline
from windrow.app import get_app, get_pipelines


logger = logging.getLogger(__name__)


router = APIRouter()
app: FastAPI = get_app()
pipelines: Dict[str, Pipeline] = get_pipelines()


@router.get("/ready")
def check_status():
    """
    This endpoint can be used during startup to understand if the
    server is ready to take any requests, or is still loading.

    The recommended approach is to call this endpoint with a short timeout,
    like 500ms, and in case of no reply, consider the server busy.
    """
    return True


@router.get("/version")
def versions():
    """
    Get the running Windrow and Haystack version.
    """
    return {"windrow": windrow_version, "haystack": None}  # haystack_version}


@router.post("/pipeline/{pipeline_name}/warmup")
def warmup(pipeline_name: str):
    pipeline = get_pipelines()[pipeline_name]

    start_time = time.time()
    pipeline.warm_up()
    logger.info(
        json.dumps(
            {"type": "warmup", "pipeline": pipeline_name, "time": f"{(time.time() - start_time):.2f}"}, default=str
        )
    )


@router.post("/pipeline/{pipeline_name}/run")
def run(pipeline_name: str, data: Dict[str, Any], parameters: Dict[str, Dict[str, Any]], debug: bool = False):
    pipeline = get_pipelines()[pipeline_name]

    start_time = time.time()
    result = pipeline.run(data=data, parameters=parameters, debug=debug)
    logger.info(
        json.dumps(
            {
                "type": "run",
                "pipeline": pipeline_name,
                "data": data,
                "parameters": parameters,
                "debug": debug,
                "response": result,
                "time": f"{(time.time() - start_time):.2f}",
            },
            default=str,
        )
    )
    return result
