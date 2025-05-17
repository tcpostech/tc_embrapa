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
from src.viticulture.enums import CategoryEnum, SubCategoryEnum
from src.viticulture.schemas import CategoryModel, CategoryCreateModel, SubCategoryModel
from src.viticulture.services import ViticultureService
from src.viticulture.utils import menus

viticulture_router = APIRouter()
access_token_bearer = AccessTokenBearer()
viticulture_service = ViticultureService()
feign_client = EmbrapaClient()


@viticulture_router.post('/external_content/{category}', status_code=status.HTTP_201_CREATED)
async def get_data_from_embrapa_by_param(category: CategoryEnum,
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
                response = await feign_client.get_external_data(client, option)

                single_category = await viticulture_service.get_category(category.name, session)
                if not single_category:
                    dict_category = CategoryCreateModel(**{'category': category.name})
                    single_category = await viticulture_service.create_category(dict_category, session)

                data_dict = await feign_client.data_to_dict(single_category, response, option)
                await viticulture_service.create_subcategories(data_dict, session)

            return {'message': 'All data saved successfully in database.'}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@viticulture_router.get('/category/{category}', response_model=CategoryModel)
async def get_by_category(category: CategoryEnum, session: AsyncSession = Depends(get_session),
                          token_details: dict = Depends(access_token_bearer)):
    """API responsible for getting all data by category"""
    result = await viticulture_service.get_category(category, session)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No data found with this category')
    return result


@viticulture_router.get('/subcategory/{subcategory}/{year}', response_model=List[SubCategoryModel])
async def get_by_subcategory(subcategory: SubCategoryEnum, year: int,
                             session: AsyncSession = Depends(get_session),
                             token_details: dict = Depends(access_token_bearer)):
    """API responsible for getting all data by subcategory and year"""
    result = await viticulture_service.get_all_subcategories(subcategory, year, session)
    if len(result) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No data found with this subcategory')
    return result
