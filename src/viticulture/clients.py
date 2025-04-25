"""
Embrapa Client class: responsible for external communication with Embrapa website
"""
import re
from io import StringIO

import pandas as pd
from fastapi import status
from fastapi.exceptions import HTTPException
from httpx import AsyncClient, Response

from src.viticulture.enums import ViticultureCategory
from src.viticulture.schemas import ViticultureCreateModel
from src.viticulture.utils import URL


class EmbrapaClient:
    """Class for processing Embrapa external communication"""

    async def process_data(self, client: AsyncClient, subcategory: str,
                           category: ViticultureCategory) -> ViticultureCreateModel:
        """
        Process all requested data and returns a valid object for database persistence
        :param client: AsyncClient variable
        :param subcategory: selected subcategory in str format
        :param category: enum ViticultureCategory
        :return: ViticultureCreateModel response
        """
        response = await client.get(url=URL.format(subcategory), timeout=10)
        if response.status_code != 200:
            error_msg = 'An error occurred during external request. Try again later!'
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=error_msg)

        result_model = await self.data_to_dict(category, response, subcategory)
        return ViticultureCreateModel(**result_model)

    async def data_to_dict(self, category: ViticultureCategory, response: Response, subcategory: str) -> dict:
        """
        Convert received data in dict
        :param category: enum ViticultureCategory
        :param response: response from AsyncClient
        :param subcategory: variable in str format
        :return: dict result
        """
        separator = ','
        if re.search('\t', response.text):
            separator = '\t'
        elif re.search(';', response.text):
            separator = ';'

        df = pd.read_csv(StringIO(response.content.decode('utf-8')), sep=separator)
        result = df.to_json(orient='records', lines=False)
        return {'category': category.name, 'subcategory': subcategory, 'data': result}
