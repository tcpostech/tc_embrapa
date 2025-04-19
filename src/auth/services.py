from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import User
from src.auth.schemas import UserCreateModel
from src.auth.utils import get_password_hash


class UserService:
    """User Service features for account registration and validation"""
    async def get_user_by_email(self, email: str, session: AsyncSession) -> User:
        """
        Get user data based in email as param
        :param email: user email in str format
        :param session: current application session
        :return: user data after get in database
        """
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()

    async def user_exists(self, email: str, session: AsyncSession):
        """
        Validate if email is already registrated in database
        :param email: user email in str format
        :param session: current application session
        :return: bool result
        """
        user = await self.get_user_by_email(email, session)
        return user is not None

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        """
        Create a new user in database with a valid UserCreateModel and returns the new User
        :param user_data: user data in UserCreateModel type format
        :param session: current application session
        :return: created user in database
        """
        user_data_dict = user_data.model_dump()
        new_user = User(**user_data_dict)
        new_user.password = get_password_hash(user_data_dict['password'])

        session.add(new_user)
        await session.commit()
        return new_user

    async def update_user(self, user: User, user_data: dict, session: AsyncSession):
        """
        Update all user data of a valid user created in database
        :param user: user already registered in database
        :param user_data: in this case only verifying User. All data shall be in dict format
        :param session: current application session
        :return: Returns the User with updated data
        """
        for k, v in user_data.items():
            setattr(user, k, v)
        await session.commit()
        return user
