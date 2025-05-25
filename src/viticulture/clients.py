"""
Embrapa Client class: responsible for external communication with Embrapa website
"""
import json
import re
from io import StringIO

import httpx
import pandas as pd
from fastapi import status
from fastapi.exceptions import HTTPException
from httpx import AsyncClient, Response
from pandas import DataFrame
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import Category
from src.viticulture.enums import CategoryEnum
from src.viticulture.schemas import CategoryCreateModel
from src.viticulture.services import ViticultureService
from src.viticulture.utils import URL, menus, FILE_PATH, new_cols

viticulture_service = ViticultureService()


class EmbrapaClient:
    """Class for processing Embrapa external communication"""

    async def process_api_mode(self, category: CategoryEnum, session: AsyncSession):
        """
        Process all data based in a selected category using external API to
        retrieve all data and persists in database
        :param category: category as Enum
        :param session: current application session
        :return:
        """
        async with httpx.AsyncClient() as client:
            try:
                for option in menus[category.name]:
                    response = await self.get_external_data(client, option)
                    single_category = await self.check_category_creation(category, session)
                    data_dict = await self.data_to_dict(single_category, response, option)
                    await viticulture_service.create_subcategories(data_dict, session)
                return {'message': 'All data saved successfully in database.'}
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e

    async def process_file_mode(self, category: CategoryEnum, session: AsyncSession):
        """
        Process all data based in a selected category using internal CSV file to
        retrieve all data and persists in database
        :param category: category as Enum
        :param session: current application session
        :return:
        """
        try:
            for option in menus[category.name]:
                with open(FILE_PATH.format(option), 'r', encoding='utf-8') as file:
                    content = file.read()
                    single_category = await self.check_category_creation(category, session)

                    separator = ','
                    if re.search('\t', content):
                        separator = '\t'
                    elif re.search(';', content):
                        separator = ';'

                    content = content.replace('\x88', '')
                    df = pd.read_csv(StringIO(content), sep=separator, engine='python')
                    data_dict = await self.process_dict(single_category, df, option)
                    await viticulture_service.create_subcategories(data_dict, session)
            return {'message': 'All data saved successfully in database.'}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e

    async def check_category_creation(self, category: CategoryEnum, session: AsyncSession):
        """
        Check if category already exists and save in database if necessary
        :param category: category as Enum
        :param session: current application session
        :return: category model
        """
        single_category = await viticulture_service.get_category(category.name, session)
        if not single_category:
            dict_category = CategoryCreateModel(**{'category': category.name})
            single_category = await viticulture_service.create_category(dict_category, session)
        return single_category

    async def get_external_data(self, client: AsyncClient, subcategory: str) -> Response:
        """
        Process all requested data and returns a valid object for database persistence
        :param client: AsyncClient variable
        :param subcategory: selected subcategory in str format
        :return: response
        """
        response = await client.get(url=URL.format(subcategory), timeout=10)
        if response.status_code != 200:
            error_msg = 'An error occurred during external request. Try again later!'
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=error_msg)
        return response

    async def data_to_dict(self, data: Category, response: Response, subcategory: str):
        """
        Convert received data in dict
        :param data: Category data
        :param response: response from AsyncClient
        :param subcategory: variable in str format
        :return: dict result
        """
        separator = ','
        if re.search('\t', response.text):
            separator = '\t'
        elif re.search(';', response.text):
            separator = ';'

        content = response.content.decode('utf-8', errors='ignore')
        content = content.replace('\x81', '')
        df = pd.read_csv(StringIO(content), sep=separator, engine='python')
        return await self.process_dict(data, df, subcategory)

    async def process_dict(self, data: Category, df: DataFrame, subcategory: str):
        """
        Switch between category mode for dictionary conversion
        :param data: Category data
        :param df: dataframe from external client
        :param subcategory: subcategory name is str
        :return: dict format
        """
        if data.category in {'IMPORTACAO', 'EXPORTACAO'}:
            return await self.process_imp_exp(data, df, subcategory)
        return await self.process_others(data, df, subcategory)

    async def process_others(self, data: Category, df: DataFrame, subcategory: str):
        """
        Process all csv data when category is not IMPORTACAO or EXPORTACAO
        :param data: Category data
        :param df: dataframe from external client
        :param subcategory: subcategory name is str
        :return: dict format
        """
        cols = df.columns.values.tolist()
        new_df = pd.melt(df, id_vars=cols[0:3], var_name='year', value_name='qty_product')
        new_df['category_uid'] = str(data.uid)
        new_df['subcategory'] = subcategory
        new_df['qty_product'] = new_df['qty_product'].replace({'nd': 0, '*': 0, '+': 0}).astype(str)
        new_df['qty_product'] = new_df['qty_product'].str.replace(',', '.').astype(float)
        new_df = new_df.rename(columns=new_cols)
        return json.loads(new_df.to_json(orient='records'))

    async def process_imp_exp(self, data: Category, df: DataFrame, subcategory: str):
        """
        Process all csv data when category is IMPORTACAO or EXPORTACAO
        :param data: Category data
        :param df: dataframe from external client
        :param subcategory: subcategory name is str
        :return: dict format
        """
        df_countries = df.iloc[:, 1:2]
        df_kg = df_countries.join(df.iloc[:, 2::2])
        df_vl = df_countries.join(df.iloc[:, 3::2])
        df_kg_melt = df_kg.melt(id_vars='País', var_name='year', value_name='qty_product')
        df_vl_melt = df_vl.melt(id_vars='País', var_name='year', value_name='vl_product')
        df_kg_melt['year'] = df_kg_melt['year'].str[:4].astype('int32')
        df_vl_melt['year'] = df_vl_melt['year'].str[:4].astype('int32')
        new_df = df_kg_melt.merge(df_vl_melt)
        new_df['category_uid'] = str(data.uid)
        new_df['subcategory'] = subcategory
        new_df = new_df.rename(columns=new_cols)
        return json.loads(new_df.to_json(orient='records'))
