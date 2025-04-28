"""
Viticulture Service: responsible for database integration
"""
from sqlmodel import select, col
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import Viticulture
from src.viticulture.schemas import ViticultureCreateModel


class ViticultureService:
    """Viticulture Service for storing Embrapa data"""

    async def create_data(self, data: ViticultureCreateModel, session: AsyncSession):
        """
        Create a new user in database with a valid ViticultureCreateModel
        and returns the new Viticulture
        :param data: data in ViticultureCreateModel type format
        :param session: current application session
        :return: created Viticulture in database
        """
        data_dict = data.model_dump()
        new_data = Viticulture(**data_dict)

        session.add(new_data)
        await session.commit()
        return new_data

    async def data_exists(self, subcategory: list[str], session: AsyncSession) -> bool:
        """
        Validate if data already exists searching by subcategory
        :param subcategory: value as list[str]
        :param session: current application session
        :return: bool result
        """
        statement = select(Viticulture).where(col(Viticulture.subcategory).in_(subcategory))
        result = await session.exec(statement)
        return len(result.all()) != 0

    async def data_from_category(self, category: str, session: AsyncSession):
        """
        Get all data by category
        :param category: ViticultureCategory in str format
        :param session: current application session
        :return: Return a list result based in the selected category
        """
        statement = select(Viticulture).where(Viticulture.category == category)
        results = await session.exec(statement)
        return results.all()

    async def data_from_subcategory(self, subcategory: str, session: AsyncSession):
        """
        Get all data by subcategory
        :param subcategory: ViticultureSubCategory in str format
        :param session: current application session
        :return: Return a list result based in the selected subcategory
        """
        statement = select(Viticulture).where(Viticulture.subcategory == subcategory)
        result = await session.exec(statement)
        return result.first()
