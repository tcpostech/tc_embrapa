"""
Viticulture Service: responsible for database integration
"""

from sqlalchemy import delete, cast, String
from sqlmodel import select, col
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import Category, SubCategory
from src.viticulture.schemas import CategoryCreateModel, SubCategoryCreateModel


class ViticultureService:
    """Viticulture Service for storing Embrapa data"""

    async def create_category(self, data: CategoryCreateModel, session: AsyncSession):
        """
        Create a new category in database with a valid CategoryCreateModel
        and returns the new Category
        :param data: data in CategoryCreateModel type format
        :param session: current application session
        :return: created Category in database
        """
        new_data = Category(**data.model_dump())
        session.add(new_data)
        await session.commit()
        return new_data

    async def create_subcategories(self, data: list, session: AsyncSession):
        """
        Create multiple subcategories in database with a dictonary
        and returns the new SubCategory
        :param data: data in dict type format
        :param session: current application session
        """
        for elem in data:
            new_sub = SubCategoryCreateModel(**elem)
            subcategory = SubCategory(**new_sub.model_dump())
            session.add(subcategory)
            await session.commit()

    async def data_exists(self, subcategory: list[str], session: AsyncSession) -> bool:
        """
        Validate if data already exists searching by subcategory
        :param subcategory: value as list[str]
        :param session: current application session
        :return: bool result
        """
        statement = select(SubCategory).where(col(SubCategory.subcategory).in_(subcategory))
        result = await session.scalars(statement)
        return len(result.all()) != 0

    async def get_category(self, category: str, session: AsyncSession):
        """
        Get all data by category as str
        :param category: Category in str format
        :param session: current application session
        :return: Return a list result based in the selected category
        """
        statement = select(Category).where(Category.category == category)
        results = await session.scalars(statement)
        return results.first()

    async def get_all_subcategories(self, subcategory: str, year: int, session: AsyncSession):
        """
        Get all data by subcategory as str and year
        :param subcategory: SubCategory in str format
        :param year: integer value
        :param session: current application session
        :return: Return a list result based in the selected subcategory
        """
        statement = (select(SubCategory).where(SubCategory.subcategory == subcategory)
                     .where(SubCategory.year == year))
        result = await session.scalars(statement)
        return result.all()

    async def delete_subcategory(self, subcategory: str, session: AsyncSession) -> dict | None:
        """
        Remove all data by subcategory as str format
        :param subcategory: subcategory in str format
        :param session: current application session
        :return: Return a dict or none
        """
        statement = delete(SubCategory).where(cast(SubCategory.subcategory, String) == subcategory)

        if statement is not None:
            await session.scalars(statement)
            await session.commit()
            return {}
        return None
