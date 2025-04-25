"""
Util class responsible JWT token validations
"""
import logging
import uuid
from datetime import datetime, timedelta

import bcrypt
import jwt
import pytz
from fastapi import status
from fastapi.exceptions import HTTPException
from itsdangerous import URLSafeTimedSerializer

from src.config import Config

serializer = URLSafeTimedSerializer(secret_key=Config.JWT_SECRET, salt='email-validation')
ACCESS_TOKEN_EXPIRY = 7200


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if the password used during login process and returns a bool result
    :param plain_password: password used in login form
    :param hashed_password: password saved in database
    :return: bool result
    """
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def get_password_hash(password: str) -> str:
    """
    Get a string password and use
    :param password: string password
    :return: hashed password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    """
    Create a jwt access token with the params below
    :param user_data: user data in dict format
    :param expiry: expiration time in seconds format (default None and not required)
    :param refresh: refresh bool value used for refreshing process (default False and not required)
    :return:
    """
    payload = {'user': user_data,
               'jti': str(uuid.uuid4()),
               'exp': datetime.now(pytz.timezone('America/Sao_Paulo')) + (
                   expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)),
               'refresh': refresh
               }

    token = jwt.encode(payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)
    return token


def decode_token(token: str) -> dict:
    """
    Decode a jwt token in str format and returns a dictionary
    :param token: jwt token in str format
    :return: dict containing values of jwt token payload
    """
    try:
        return jwt.decode(jwt=token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid or expired token.') from e


def create_url_safe_token(data: dict):
    """
    Generate a secured token for account validation with itsdangerous library
    :param data: user account basic data for serialization with itsdangerous
    :return: returns a token for account activation
    """
    return serializer.dumps(data)


def decode_url_safe_token(token: str):
    """
    Validate and decode a valid token for account activation
    :param token: token in str format
    :return:
    """
    try:
        return serializer.loads(token)
    except Exception as e:
        logging.error(str(e))
        return None
