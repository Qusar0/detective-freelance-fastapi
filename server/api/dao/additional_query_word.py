from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List

from server.api.dao.base import BaseDAO
from server.api.models.models import AdditionalQueryWord, AdditionalQueryWordType


class AdditionalQueryWordDAO(BaseDAO):
    model = AdditionalQueryWord

    @classmethod
    async def add_words(
        cls,
        db: AsyncSession,
        query_id: int,
        words: str,
        word_type: str,
    ) -> bool:
        try:
            type_query = select(AdditionalQueryWordType.id).where(
                AdditionalQueryWordType.query_word_type == word_type
            )
            type_result = await db.execute(type_query)
            word_type_id = type_result.scalar_one_or_none()

            if not word_type_id:
                logger.error(f"Тип слова '{word_type}' не найден")
                return False

            if isinstance(words, str):
                delimiter = '+' if word_type == 'plus' else '+-'
                word_list = [word for word in words.split(delimiter) if word.strip()]
            else:
                word_list = words

            if not word_list:
                logger.error(f"Не найдено слов для добавления для типа {word_type} и слов {words}")
                return False

            for word in word_list:
                new_word = AdditionalQueryWord(
                    query_id=query_id,
                    query_word=word.strip(),
                    query_word_type_id=word_type_id
                )
                db.add(new_word)

            await db.commit()
            return True

        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"Ошибка при добавлении дополнительных слов: {e}")
            return False
        except Exception as e:
            logger.error(f"Неожиданная ошибка: {e}")
            return False

    @classmethod
    async def get_words_by_query(
        cls,
        db: AsyncSession,
        query_id: int,
        word_type: Optional[str] = None
    ) -> list[AdditionalQueryWord]:
        try:
            query = select(AdditionalQueryWord).where(
                AdditionalQueryWord.query_id == query_id,
            )

            if word_type:
                query = query.join(AdditionalQueryWord.query_word_type).where(
                    AdditionalQueryWordType.query_word_type == word_type,
                )

            result = await db.execute(query)
            return list(result.scalars())

        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении дополнительных слов: {e}")
            return []

    @classmethod
    async def get_query_words_by_type(
        cls,
        query_id: int,
        word_type: str,
        db: AsyncSession
    ) -> List[str]:
        """Получает дополнительные слова заданного типа для запроса"""
        try:
            result = await db.execute(
                select(AdditionalQueryWord.query_word)
                .join(AdditionalQueryWord.query_word_type)
                .where(
                    AdditionalQueryWord.query_id == query_id,
                    AdditionalQueryWordType.query_word_type == word_type
                )
            )
            return [word[0] for word in result.all()]
        except SQLAlchemyError as e:
            logger.error(f"Ошибка получения категории слов '{word_type}': {e}")
            raise
