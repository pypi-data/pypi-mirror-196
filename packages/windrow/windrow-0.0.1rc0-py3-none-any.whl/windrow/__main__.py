import logging

import uvicorn

from windrow.app import get_app

logger = logging.getLogger(__name__)

logger.info("Open http://127.0.0.1:8000/docs to see the API Documentation.")
logger.info(
    "Or just try it out directly: curl --request POST --url 'http://127.0.0.1:8000/query_pipeline/run' "
    '-H "Content-Type: application/json"  --data \'{"query": "Who is the father of Arya Stark?"}\''
)


if __name__ == "__main__":
    uvicorn.run(get_app(), host="0.0.0.0", port=8000)
