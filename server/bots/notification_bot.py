from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy import select
from typing import Any, Callable, Coroutine
from functools import wraps
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
        logger.info(f"Уведомление отправлено в чат {chat_id}")
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления: {e}")


class BalanceNotifier:
    _notified_services = set()

    @classmethod
    def notify_balance(cls, func: Callable[..., Coroutine[Any, Any, Any]]):
        """Улучшенный декоратор для уведомлений о балансе"""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            original_result = await func(*args, **kwargs)

            try:
                async with async_session() as session:
                    result = await session.execute(select(ServicesBalance))
                    services = result.scalars().all()

                    for service in services:
                        if service.balance is None:
                            continue

                        if all([
                            service.balance < service.balance_threshold,
                            service.service_name not in cls._notified_services
                        ]):
                            message = (
                                f"⚠️ <strong>Внимание!</strong> Баланс сервиса <strong>{service.service_name}</strong> "
                                f"опустился ниже <strong>{service.balance_threshold}</strong>. \
                                Текущий баланс: <strong>{service.balance}</strong>"
                            )
                            await send_balance_alert(settings.admin_chat_id, message)
                            cls._notified_services.add(service.service_name)
                        elif all([
                            service.balance >= service.balance_threshold,
                            service.service_name in cls._notified_services
                        ]):
                            cls._notified_services.remove(service.service_name)
            except Exception as e:
                logger.error(f"Balance check error: {e}")

            return original_result

        return wrapper


if __name__ == "__main__":
    try:
        from aiogram import executor
        executor.start_polling(dp, skip_updates=True)
    except KeyboardInterrupt:
        logger.info("🛑 Бот остановлен вручную")
    except Exception as e:
        logger.error(f"🚨 Ошибка при запуске бота: {e}")
