import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from server.api.models.models import Users, Language


class UserLanguageDAO:
    """DAO для работы с языками пользователей"""

    @staticmethod
    async def get_user_default_language(db: AsyncSession, user_id: int) -> str:
        """Получает код языка по умолчанию пользователя."""
        try:
            result = await db.execute(
                select(Users.default_language_id)
                .where(Users.id == user_id)
            )
            default_language_id = result.scalar_one_or_none()

            if default_language_id is None:
                return 'ru'

            lang_result = await db.execute(
                select(Language.code)
                .where(Language.id == default_language_id)
            )
            language_code = lang_result.scalar_one_or_none()

            return language_code or 'ru'
        except (SQLAlchemyError, Exception) as e:
            logging.error(f"Ошибка при получении языка пользователя: {e}")
            return 'ru'

    @staticmethod
    async def set_user_default_language(db: AsyncSession, user_id: int, language_code: str) -> bool:
        """Устанавливает язык по умолчанию пользователя по коду языка."""
        try:
            lang_result = await db.execute(
                select(Language)
                .where(Language.code == language_code)
            )
            language = lang_result.scalar_one_or_none()
            if not language:
                logging.warning(f"Язык с кодом {language_code} не найден")
                return False

            await db.execute(
                update(Users)
                .where(Users.id == user_id)
                .values(default_language_id=language.id)
            )
            await db.commit()
            return True
        except (SQLAlchemyError, Exception) as e:
            logging.error(f"Ошибка при обновлении языка пользователя: {e}")
            await db.rollback()
            return False
