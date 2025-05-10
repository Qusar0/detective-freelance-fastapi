from aiogram import Bot, Dispatcher
from aiogram.types import Message, ParseMode
import asyncio
from server.api.conf.config import settings

bot = Bot(token=settings.notification_bot_token, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_connects(message: Message):
    chat_id = message.chat.id
    url = f"{settings.frontend_url}/api/connect_tg?chat={chat_id}"
    await message.reply(f"Привет, для подписки на уведомления перейди по ссылке: {url}")


async def send_notification(chat_id: int, text: str):
    await bot.send_message(chat_id, f'Ваш запрос по этому объекту "{text}" обработан')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
