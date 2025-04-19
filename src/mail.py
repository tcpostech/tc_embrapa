from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType

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
