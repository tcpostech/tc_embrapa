from datetime import datetime, timedelta

from fastapi import APIRouter, status, Depends, BackgroundTasks
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.dependencies import RefreshTokenBearer, get_current_user
from src.auth.schemas import UserCreateModel, UserLoginModel, UserModel
from src.auth.services import UserService
from src.auth.utils import create_url_safe_token, create_access_token, verify_password, decode_url_safe_token
from src.db.main import get_session
from src.mail import mail_config, welcome_message

auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIRY = 2


@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, bg_tasks: BackgroundTasks,
                              session: AsyncSession = Depends(get_session)):
    """Allows a user make a new registration before using the other API resources"""
    user_exists = await user_service.user_exists(user_data.email, session)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'User with email ({user_data.email}) already exists')
    new_user = await user_service.create_user(user_data, session)
    token = create_url_safe_token({'email': user_data.email})

    message = welcome_message(user_data, token)
    bg_tasks.add_task(mail_config.send_message, message)
    return {'message': 'Account created! Check your email to verify your account', "user": new_user}


@auth_router.post('/login')
async def login_user(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    """Allow a user login the application after email verification"""
    user = await user_service.get_user_by_email(login_data.email, session)
    if user is not None:
        msg = 'You need to validate your account before login. Please, check your email!'
        if not user.is_verified:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=msg)

        password_valid = verify_password(login_data.password, user.password)
        if password_valid:
            user_data = {'email': user.email, 'user_uid': str(user.uid)}
            access_token = create_access_token(user_data=user_data)
            refresh_token = create_access_token(user_data=user_data, refresh=True,
                                                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY))

            return JSONResponse(content={'message': 'Login successful', 'access_token': access_token,
                                         'refresh_token': refresh_token, 'user': user_data})
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid email or password.')


@auth_router.post('/refresh_token')
async def refresh_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    """Allows a jwt token revalidation with a valid refresh token"""
    expiry_timestamp = token_details['exp']

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details['user'])
        return JSONResponse(content={'access_token': new_access_token})

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid or expired token.')


@auth_router.get('/verify/{token}')
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):
    """Allows a user verification after the registration process"""
    token_data = decode_url_safe_token(token)
    user_email = token_data.get('email')

    if user_email:
        user = await user_service.get_user_by_email(user_email, session)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        await user_service.update_user(user, {'is_verified': True}, session)
        return JSONResponse(
            content={'message': 'Account verified successfully'},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={'message': 'Error occurred during verification'},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@auth_router.get('/me', response_model=UserModel)
async def get_current_user_data(user=Depends(get_current_user)):
    """Return the current logged user based in the current valid JWT token"""
    return user
