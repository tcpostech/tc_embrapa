from fastapi import FastAPI

from src.auth.routes import auth_router
from src.client.routes import client_router

app = FastAPI(
    version='1.0.0',
    title='Tech Challenge 01 - Collection API',
    description='A Rest API collection for FIAP - Tech Challenge'
)

app.include_router(auth_router, prefix='/v1/api/auth', tags=['Auth Controller'])
app.include_router(client_router, prefix='/v1/api', tags=['External Client Controller'])
