from io import StringIO

import pandas as pd
from fastapi import status
from fastapi.exceptions import HTTPException
from httpx import AsyncClient, Response

from src.client.enums import EmbrapaParams
from src.client.schemas import ViticultureCreateModel
from src.client.utils import url


class EmbrapaClient:
    """Class for processing Embrapa external communication"""

    async def process_data(self, client: AsyncClient, subcategory: str,
                           param: EmbrapaParams) -> ViticultureCreateModel:
        """
        Process all requested data and returns a valid object for database persistence
        :param client: AsyncClient variable
        :param subcategory: selected subcategory in str format
        :param param: enum EmbrapaParams
        :return: ViticultureCreateModel response
        """
        response = await client.get(url=url.format(subcategory), timeout=10)
        if response.status_code != 200:
            error_msg = 'An error occurred during external request. Try again later!'
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=error_msg)
        response.encoding = 'utf-8'

        result_model = await self.data_to_dict(param, response, subcategory)
        return ViticultureCreateModel(**result_model)

    async def data_to_dict(self, param: EmbrapaParams, response: Response, subcategory: str) -> dict:
        """
        Convert received data in dict
        :param param: enum EmbrapaParams
        :param response: response from AsyncClient
        :param subcategory: variable in str format
        :return: dict result
        """
        df = pd.read_csv(StringIO(response.text), sep=';', encoding='utf8')
        result = df.to_json(orient='records', lines=False)
        return {'category': param.name, 'subcategory': subcategory, 'data': result}
