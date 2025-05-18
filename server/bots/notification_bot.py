import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy import select
import asyncio

from server.api.conf.config import settings
from server.api.database.database import async_session
from server.api.models.models import ServicesBalance


bot = Bot(token=settings.notification_bot_token, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def send_connects(message: Message):
    chat_id = message.chat.id
    url = f"{settings.frontend_url}/connect_tg?chat={chat_id}"
    await message.reply(f"Привет, для подписки на уведомления перейди по ссылке: {url}")


async def send_notification(chat_id: int, text: str):
    await bot.send_message(chat_id, f'Ваш запрос по этому объекту "{text}" обработан')


async def send_balance_alert(chat_id: int, text: str):
    try:
        await bot.send_message(chat_id, text)
        logging.info(f"Уведомление отправлено в чат {chat_id}")
    except Exception as e:
        logging.error(f"Ошибка при отправке уведомления: {e}")


async def check_balances():
    """Проверяет балансы сервисов и отправляет уведомления, если баланс ниже порога."""
    try:
        async with async_session() as session:
            result = await session.execute(select(ServicesBalance))
            services = result.scalars().all()
            
            for service in services:
                if service.balance is not None and service.balance < settings.balance_threshold:
                    message = (
                        f"⚠️ <strong>Внимание!</strong> Баланс сервиса `{service.service_name}` "
                        f"опустился ниже `{settings.balance_threshold}`. Текущий баланс: `{service.balance}`"
                    )
                    await send_balance_alert(settings.admin_chat_id, message)
    except Exception as e:
        logging.error(f"Ошибка при проверке балансов: {e}")


async def periodic_balance_check():
    """Запускает проверку балансов каждые 3 часа."""
    while True:
        logging.info(f"🔍 Проверка балансов...")
        await check_balances()
        await asyncio.sleep(settings.check_interval)


async def on_startup(_):
    """Запускает периодическую проверку при старте бота."""
    asyncio.create_task(periodic_balance_check())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        from aiogram import executor
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    except KeyboardInterrupt:
        logging.info("🛑 Бот остановлен вручную")
    except Exception as e:
        logging.error(f"🚨 Ошибка при запуске бота: {e}")
    


