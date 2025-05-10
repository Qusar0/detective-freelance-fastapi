from email.message import EmailMessage
from aiosmtplib import send
from server.api.conf.config import settings
from itsdangerous import URLSafeTimedSerializer
from server.api.templates.email_message import get_confirmation_email
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from server.api.models.models import Users


async def send_email(
    subject: str,
    recipients: list[str],
    body: str,
    html: str = None,
):
    message = EmailMessage()
    message["From"] = f"{settings.mail_from_name} <{settings.mail_from}>"
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject
    message.set_content(body)

    if html:
        message.add_alternative(html, subtype="html")

    await send(
        message,
        hostname=settings.mail_server,
        port=settings.mail_port,
        username=settings.mail_username,
        password=settings.mail_password,
        start_tls=True,
    )


def generate_conformation_token(email):
    serializer = URLSafeTimedSerializer(settings.secret_key)

    return serializer.dumps(email, salt=settings.security_password_salt)


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(settings.secret_key)
    try:
        email = serializer.loads(
            token,
            salt=settings.security_password_salt,
            max_age=expiration
        )
    except Exception:
        return False
    return email


async def check_user_confirmation(user_id: int, db: AsyncSession) -> bool:
    result = await db.execute(
        select(Users)
        .where(Users.id == user_id),
    )
    user = result.scalar_one_or_none()
    if not user:
        return False
    return user.is_confirmed


async def send_confirmation_email(user: Users):
    token = generate_conformation_token(user.email)
    confirm_url = f'{settings.frontend_url}/confirm-email?token={token}'
    email_content = get_confirmation_email(user.email, confirm_url)
    await send_email(**email_content)
