import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional

from server.api.dao.base import BaseDAO
from server.api.models.models import Keywords, KeywordType
from server.api.services.text import translate_words


class KeywordsDAO(BaseDAO):
    model = Keywords

    @classmethod
    async def _get_keywords_by_types(
        cls,
        db: AsyncSession,
        kwd_types: List[str],
    ) -> tuple[int, dict]:
        counter = 0
        named_keywords = {}
        
        for kwd_type in kwd_types:
            query = (
                select(Keywords.word)
                .join(Keywords.keyword_type)
                .where(KeywordType.keyword_type_name == kwd_type)
            )
            result = await db.execute(query)
            keywords = [kwd for kwd in result.scalars()]
            counter += len(keywords)
            named_keywords[kwd_type] = keywords
            
        return counter, named_keywords

    @classmethod
    async def get_default_keywords(
        cls,
        db: AsyncSession,
        default_keywords_type: str,
        languages: Optional[List[str]] = None,
    ):
        if not languages:
            languages = ['ru']

        splitted_kws = default_keywords_type.split(", ")
        
        if '' in splitted_kws:
            return (0, {lang: {} for lang in languages})

        try:
            if 'report' in splitted_kws:
                kwd_types = ['reputation', 'negativ', 'relations']
            elif 'company_report' in splitted_kws:
                kwd_types = ['company_reputation', 'company_negativ', 'company_relations']
            else:
                kwd_types = splitted_kws

            counter, named_keywords = await cls._get_keywords_by_types(db, kwd_types)

            translated_words = translate_words(
                keywords_by_category=named_keywords,
                target_languages=languages,
            )
            coefficient = len(languages) or 1
            return (counter * coefficient, translated_words)
        except (SQLAlchemyError, Exception) as e:
            logging.error(f"Ошибка при получении ключевых слов: {e}")

    @classmethod
    async def get_keyword_type_id(
        cls,
        db: AsyncSession,
        keyword_type: str
    ) -> Optional[int]:
        """Получает ID типа ключевого слова по его названию"""
        try:
            query = select(KeywordType.id).where(
                KeywordType.keyword_type_name == keyword_type
            )
            result = await db.execute(query)
            return result.scalar_one_or_none()
            
        except SQLAlchemyError as e:
            logging.error(f"Ошибка при получении ID типа ключевого слова: {e}")
            return None
