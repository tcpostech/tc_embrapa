import httpx
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import AccessTokenBearer
from src.client.enums import EmbrapaParams
from src.client.utils import menus, url
from src.db.main import get_session

embrapa_router = APIRouter()
access_token_bearer = AccessTokenBearer()


@embrapa_router.get('/embrapa/external_content/{param}')
async def get_data_from_embrapa_by_param(param: EmbrapaParams,
                                         session: AsyncSession = Depends(get_session),
                                         token_details: dict = Depends(access_token_bearer)):
    """
    API responsible for download all CSV files from
    Embrapa website based in each category param
    """
    async with httpx.AsyncClient() as client:
        for option in menus[param.name]:
            response = await client.get(url=url.format(option))
            if response.status_code != 200:
                error_msg = 'An error occurred during external request. Try again later!'
                raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=error_msg)
    pass
