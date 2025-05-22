"""
Main class of the application.
All configuration below is used for Controller additions, cors configuration,
Swagger and Redoc headers, etc.
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.auth.routes import auth_router
from src.middleware import register_middleware
from src.viticulture.routes import viticulture_router

tags_metadata = [
    {
        "name": "Auth Controller",
        "description": "Methods responsible for handling auth and user features"
    }, {
        "name": "Viticulture Controller",
        "description": """Methods responsible for getting Embrapa data, 
        persisting in database and retrieve all viticulture saved data"""
    }
]

app = FastAPI(
    version='1.0.0',
    title='Tech Challenge 01 - Collection API',
    description='A Rest API collection for FIAP - Tech Challenge',
    terms_of_service='#',
    license_info={"name": "Apache 2.0", "url": "https://www.apache.org/licenses/LICENSE-2.0"},
    redoc_url='/documentation/redoc',
    docs_url='/documentation/swagger',
    openapi_url='/documentation/openapi.json',
    openapi_tags=tags_metadata
)

app.mount("/site", StaticFiles(directory="site"), name="docs")
app.mount("/assets", StaticFiles(directory='site/assets'), name='assets')
app.mount("/search", StaticFiles(directory='site/search'), name='search')
templates = Jinja2Templates(directory="site")


@app.get("/", include_in_schema=False)
async def mkdocs(request: Request):
    """Exposing api documentation and excluding from swagger and redoc"""
    return templates.TemplateResponse(name="index.html", request=request)


register_middleware(app)
app.include_router(auth_router, prefix='/v1/api/auth', tags=['Auth Controller'])
app.include_router(viticulture_router, prefix='/v1/api/viticulture', tags=['Viticulture Controller'])
