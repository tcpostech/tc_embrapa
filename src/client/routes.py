import httpx
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.responses import JSONResponse

from src.auth.dependencies import AccessTokenBearer
from src.client.enums import EmbrapaParams
from src.client.embrapa_client import EmbrapaClient
from src.client.services import ViticultureService
from src.client.utils import menus
from src.db.main import get_session

client_router = APIRouter()
access_token_bearer = AccessTokenBearer()
viticulture_service = ViticultureService()
feign_client = EmbrapaClient()


@client_router.get('/embrapa/external_content/{category}')
async def get_data_from_embrapa_by_param(category: EmbrapaParams,
                                         session: AsyncSession = Depends(get_session),
                                         token_details: dict = Depends(access_token_bearer)):
    """
    API responsible for download all CSV files from Embrapa website based
    on each category param and save in database
    """
    exists = await viticulture_service.data_exists(menus[category.name], session)
    if exists:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,
                            detail='All data already exists in database.')

    async with httpx.AsyncClient() as client:
        try:
            for option in menus[category.name]:
                viticulture = await feign_client.process_data(client, option, category)
                await viticulture_service.create_data(viticulture, session)
            return JSONResponse(content={'message': 'All data saved successfully in database'})
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
