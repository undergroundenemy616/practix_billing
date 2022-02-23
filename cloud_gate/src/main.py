import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api import payments
from core.logger import LOGGING

logger = logging.getLogger(__name__)
logging.config.dictConfig(LOGGING)

app = FastAPI(
    title='Cloud Payments API emulator',
    version='1.0.0',
    description='Asynchronous API to handle notification templates',
    docs_url='/api/docs',
    openapi_url='/api/openapi.json',
    redoc_url='/api/redoc',
    default_response_class=ORJSONResponse,
)


app.include_router(payments.router, prefix='/payments', tags=['Payment'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8888,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
