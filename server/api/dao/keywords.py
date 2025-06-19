import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from server.api.dao.base import BaseDAO
from server.api.models.models import Keywords
from server.api.services.text import translate_words


class KeywordsDAO(BaseDAO):
    model = Keywords

    @classmethod
    async def get_default_keywords(
        cls,
        db: AsyncSession,
        default_keywords_type: str,
        languages: List[str] = None,
    ):
        if not languages:
            languages = ['ru']
        splitted_kws = default_keywords_type.split(", ")
        named_keywords = {}
        counter = 0

        if '' in splitted_kws:
            return (counter, {lang: {} for lang in languages})

        if 'report' in splitted_kws:
            types_belongs_report = ['reputation', 'negativ', 'relations']
            for kwd_type in types_belongs_report:
                query = select(Keywords.word).filter_by(word_type=kwd_type)
                result = await db.execute(query)
                keywords = [kwd for kwd in result.scalars()]
                counter += len(keywords)
                named_keywords[kwd_type] = keywords
        elif 'company_report' in splitted_kws:
            types_belongs_report = ['company_reputation', 'company_negativ', 'company_relations']
            for kwd_type in types_belongs_report:
                query = select(Keywords.word).filter_by(word_type=kwd_type)
                result = await db.execute(query)
                keywords = [kwd for kwd in result.scalars()]
                counter += len(keywords)
                named_keywords[kwd_type] = keywords
        else:
            for splitted_kwd in splitted_kws:
                query = select(Keywords.word).filter_by(word_type=splitted_kwd)
                result = await db.execute(query)
                keywords = [kwd for kwd in result.scalars()]
                counter += len(keywords)
                named_keywords[splitted_kwd] = keywords

        translated_words = translate_words(
            keywords_by_category=named_keywords,
            target_languages=languages,
        )
        coefficient = len(languages) or 1
        return (counter * coefficient, translated_words)