from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType

from src.auth.schemas import UserCreateModel
from src.config import Config

conn_config = ConnectionConfig(
    MAIL_USERNAME=Config.MAIL_USERNAME,
    MAIL_PASSWORD=Config.MAIL_PASSWORD,
    MAIL_FROM=Config.MAIL_FROM,
    MAIL_PORT=Config.MAIL_PORT,
    MAIL_SERVER=Config.MAIL_SERVER,
    MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
    MAIL_STARTTLS=Config.MAIL_STARTTLS,
    MAIL_SSL_TLS=Config.MAIL_SSL_TLS,
    USE_CREDENTIALS=Config.USE_CREDENTIALS,
    VALIDATE_CERTS=Config.VALIDATE_CERTS
)

mail_config = FastMail(config=conn_config)


def create_message(recipients: list, subject: str, body: str):
    """
    This method is responsible for generate an email template with MessageSchema and the params below
    :param recipients: a list[str] of emails
    :param subject: the email subject
    :param body: the email content
    :return: the email template that will be sent with the method send_message in mail_config
    """
    return MessageSchema(recipients=recipients, subject=subject, body=body, subtype=MessageType.html)


def welcome_message(user: UserCreateModel, token: str):
    """Generate a welcome message ready for sending by email"""
    subject = f'Welcome to {Config.MAIL_FROM_NAME}! Confirm Your Registration'
    link = f'http://{Config.DOMAIN_URL}/v1/api/auth/verify/{token}'

    message = f"""
    <h1>Dear {user.first_name},</h1>

    <p>Thank you for registering with {Config.MAIL_FROM_NAME}! We're excited to have you on board.</p>

    <p>To complete your registration, please click the link below to confirm your email address 
    and activate your account:</p>

    <a href="{link}">Confirm Registration</a>

    <p>If the link above doesn’t work, you can copy and paste this URL into your browser:</p>
    <p>{link}</p>

    <p>If you did not sign up for an account, please ignore this email.</p>

    <p>Looking forward to seeing you inside!</p>
    <p>Best regards, {Config.MAIL_FROM_NAME}</p>
    """
    return create_message([user.email], subject, message)
