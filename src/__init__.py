from fastapi import FastAPI

from src.auth.routes import auth_router

app = FastAPI(
    version='1.0.0',
    title='Tech Challenge - Embrapa Collection API',
    description='A Rest API collection for FIAP - Tech Challenge'
)

app.include_router(auth_router, prefix='/v1/api/auth', tags=['Auth Controller'])
