"""
Viticulture Controller: responsible for getting all Embrapa viticulture data
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import AccessTokenBearer
from src.db.main import get_session
from src.viticulture.clients import EmbrapaClient
from src.viticulture.enums import CategoryEnum, SubCategoryEnum, ProcessModeEnum
from src.viticulture.schemas import CategoryModel, SubCategoryModel
from src.viticulture.services import ViticultureService
from src.viticulture.utils import menus

viticulture_router = APIRouter()
access_token_bearer = AccessTokenBearer()
viticulture_service = ViticultureService()
feign_client = EmbrapaClient()


@viticulture_router.post('/external_content/{category}', status_code=status.HTTP_201_CREATED)
async def get_data_from_embrapa_by_param(category: CategoryEnum,
                                         mode: Optional[ProcessModeEnum] = ProcessModeEnum.API,
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

    if mode == ProcessModeEnum.FILE:
        return await feign_client.process_file_mode(category, session)
    return await feign_client.process_api_mode(category, session)


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
