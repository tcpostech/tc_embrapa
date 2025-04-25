"""
Viticulture Controller: responsible for getting all Embrapa viticulture data
"""
from typing import List

import httpx
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import AccessTokenBearer
from src.db.main import get_session
from src.viticulture.clients import EmbrapaClient
from src.viticulture.enums import ViticultureCategory, ViticultureSubCategory
from src.viticulture.schemas import ViticultureModel
from src.viticulture.services import ViticultureService
from src.viticulture.utils import menus

viticulture_router = APIRouter()
access_token_bearer = AccessTokenBearer()
viticulture_service = ViticultureService()
feign_client = EmbrapaClient()


@viticulture_router.post('/external_content/{category}', status_code=status.HTTP_201_CREATED)
async def get_data_from_embrapa_by_param(category: ViticultureCategory,
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
            return {'message': 'All data saved successfully in database.'}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@viticulture_router.get('/category/{category}', response_model=List[ViticultureModel])
async def get_by_category(category: ViticultureCategory, session: AsyncSession = Depends(get_session),
                          token_details: dict = Depends(access_token_bearer)):
    """API responsible for getting all data by category"""
    results = await viticulture_service.data_from_category(category, session)
    if len(results) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No data found with this category')
    return results


@viticulture_router.get('/subcategory/{subcategory}', response_model=ViticultureModel)
async def get_by_subcategory(subcategory: ViticultureSubCategory,
                             session: AsyncSession = Depends(get_session),
                             token_details: dict = Depends(access_token_bearer)):
    """API responsible for getting all data by subcategory"""
    result = await viticulture_service.data_from_subcategory(subcategory, session)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No data found with this subcategory')
    return result
