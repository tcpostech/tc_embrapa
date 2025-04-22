from fastapi import FastAPI

from src.auth.routes import auth_router
from src.middleware import register_middleware
from src.viticulture.routes import viticulture_router

app = FastAPI(
    version='1.0.0',
    title='Tech Challenge 01 - Collection API',
    description='A Rest API collection for FIAP - Tech Challenge'
)

register_middleware(app)
app.include_router(auth_router, prefix='/v1/api/auth', tags=['Auth Controller'])
app.include_router(viticulture_router, prefix='/v1/api/viticulture', tags=['Viticulture Controller'])
