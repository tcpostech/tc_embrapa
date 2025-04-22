import logging
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.requests import Request

from src.config import Config

logger = logging.getLogger('uvicorn.access')
logger.disabled = True


def register_middleware(app: FastAPI):
    """Cors config middleware"""
    @app.middleware('http')
    async def custom_logging(req: Request, call_next):
        begin = time.time()
        res = await call_next(req)
        total_time = time.time() - begin
        host = req.client.host
        port = req.client.port
        code = res.status_code
        msg = f'{host}:{port} - {req.method} - {req.url.path} - {code} after {total_time}'
        print(msg)
        return res

    app.add_middleware(CORSMiddleware,
                       allow_origins=['*'],
                       allow_methods=['GET', 'POST', 'PATCH', 'DELETE', 'OPTION', 'PUT'],
                       allow_headers=['*'],
                       allow_credentials=True)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=['localhost', '127.0.0.1', Config.DOMAIN_URL])
