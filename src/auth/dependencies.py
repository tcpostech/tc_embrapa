from fastapi import Request, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.services import UserService
from src.auth.utils import decode_token
from src.db.main import get_session

user_service = UserService()


class TokenBearer(HTTPBearer):
    """Token Bearer features"""
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | dict | None:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_token(token)

        if not self.token_valid(token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
                'error': 'This token is invalid or expired',
                'resolution': 'Please get new token'
            })
        self.verify_token_data(token_data)
        return token_data

    def token_valid(self, token: str) -> bool:
        """
        Check if jwt token is valid or not
        :param token: token in str format
        :return: Result as bool value
        """
        return decode_token(token) is not None

    def verify_token_data(self, token_data):
        """Default method without implementation"""
        raise NotImplementedError('Please override this method in child classes')


class AccessTokenBearer(TokenBearer):
    """AccessTokenBearer features for token validations"""
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail='Please provide an access token')


class RefreshTokenBearer(TokenBearer):
    """RefreshTokenBearer features for token validations"""
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail='Please provide a refresh token')


async def get_current_user(token_details: dict = Depends(AccessTokenBearer()),
                           session: AsyncSession = Depends(get_session)):
    """
    Receive an extracted data from jwt token and after search in database it returns the user data
    :param token_details: extracted jwt token payload in dict format
    :param session: current application session
    :return: user data after get in database
    """
    user_email = token_details['user']['email']
    return await user_service.get_user_by_email(user_email, session)
