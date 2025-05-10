from aiogram import Bot
from aiogram.types import ParseMode
from server.api.conf.config import settings


bot = Bot(token=settings.support_bot_token, parse_mode=ParseMode.HTML)

SUPPORT_CHAT_ID = 637166903


async def send_message_async(theme: str, description: str, contacts: str):
    text = (
        f"<b>Тема:</b> {theme}\n"
        f"<b>Описание:</b> {description}\n"
        f"<b>Контакты:</b> {contacts}"
    )
    await bot.send_message(chat_id=SUPPORT_CHAT_ID, text=text)
