from aiogram import Bot, Dispatcher
from aiogram.types import Message, ParseMode
import asyncio

API_TOKEN = "7998886482:AAGjvLBeMR2r9KBcmYMz9wb_uGNm5d_L8jM"

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_connects(message: Message):
    chat_id = message.chat.id
    url = f"http://ias-detective.io/api/connect_tg?chat={chat_id}"
    await message.reply(f"Привет, для подписки на уведомления перейди по ссылке: {url}")


async def send_notification(chat_id: int, text: str):
    await bot.send_message(chat_id, f'Ваш запрос по этому объекту "{text}" обработан')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
