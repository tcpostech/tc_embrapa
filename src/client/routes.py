from io import StringIO

import httpx
import pandas as pd
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.responses import JSONResponse

from src.auth.dependencies import AccessTokenBearer
from src.client.enums import EmbrapaParams
from src.client.schemas import ViticultureCreateModel
from src.client.services import ViticultureService
from src.client.utils import menus, url
from src.db.main import get_session

client_router = APIRouter()
access_token_bearer = AccessTokenBearer()
viticulture_service = ViticultureService()


@client_router.get('/embrapa/external_content/{param}')
async def get_data_from_embrapa_by_param(param: EmbrapaParams,
                                         session: AsyncSession = Depends(get_session),
                                         token_details: dict = Depends(access_token_bearer)):
    """
    API responsible for download all CSV files from Embrapa website based
    on each category param and save in database
    """
    async with httpx.AsyncClient() as client:
        exists = await viticulture_service.data_exists(menus[param.name], session)
        if exists:
            raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,
                                detail='All data already exists in database.')

        try:
            for option in menus[param.name]:
                response = await client.get(url=url.format(option), timeout=10)
                if response.status_code != 200:
                    error_msg = 'An error occurred during external request. Try again later!'
                    raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=error_msg)
                response.encoding = 'utf-8'
                df = pd.read_csv(StringIO(response.text), sep=';', encoding='utf8')
                result = df.to_json(orient='records', lines=False)

                result_model = {'category': param.name, 'subcategory': option, 'data': result}
                viticulture = ViticultureCreateModel(**result_model)
                await viticulture_service.create_data(viticulture, session)
            return JSONResponse(content={'message': 'All data saved successfully in database'})
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
