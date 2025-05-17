"""
Embrapa Client class: responsible for external communication with Embrapa website
"""
import json
import re
from io import StringIO

import pandas as pd
from fastapi import status
from fastapi.exceptions import HTTPException
from httpx import AsyncClient, Response
from pandas import DataFrame

from src.db.models import Category
from src.viticulture.utils import URL


class EmbrapaClient:
    """Class for processing Embrapa external communication"""

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
        :param data: enum Category
        :param response: response from AsyncClient
        :param subcategory: variable in str format
        :return: dict result
        """
        new_cols = {'cultivar': 'product', 'País': 'country', 'produto': 'product'}

        separator = ','
        if re.search('\t', response.text):
            separator = '\t'
        elif re.search(';', response.text):
            separator = ';'

        content = response.content.decode('utf-8', errors='ignore')
        content = content.replace('\x88', '')
        df = pd.read_csv(StringIO(content), sep=separator, engine='python')

        if data.category in {'IMPORTACAO', 'EXPORTACAO'}:
            return await self.process_imp_exp(data, df, new_cols, subcategory)
        return await self.process_others(data, df, new_cols, subcategory)

    async def process_others(self, data: Category, df: DataFrame, new_cols: dict, subcategory: str):
        """
        Process all csv data when category is not IMPORTACAO or EXPORTACAO
        :param data: Category data
        :param df: dataframe from external client
        :param new_cols: new columns to rename
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

    async def process_imp_exp(self, data: Category, df: DataFrame, new_cols: dict, subcategory: str):
        """
        Process all csv data when category is IMPORTACAO or EXPORTACAO
        :param data: Category data
        :param df: dataframe from external client
        :param new_cols: new columns to rename
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
