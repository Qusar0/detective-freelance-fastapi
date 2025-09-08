from celery import shared_task
from loguru import logger
from server.api.IRBIS_parser.arbitration_court import ArbitrationCourt
from server.api.IRBIS_parser.bankruptcy import Bankruptcy
from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS
from server.api.IRBIS_parser.corruption import Corruption
from server.api.IRBIS_parser.court_of_general_jurisdiction import CourtGeneralJurisdiction
from server.api.IRBIS_parser.pledgess import Pledges
from server.api.IRBIS_parser.disqualified_persons import DisqualifiedPersons
from server.api.IRBIS_parser.fssp import FSSP
from server.api.IRBIS_parser.ml_index import MLIndex
from server.api.IRBIS_parser.participation_in_organization import ParticipationOrganization
from server.api.IRBIS_parser.tax_arrears import TaxArrears
from server.api.IRBIS_parser.terror_list import TerrorList
from server.api.models.irbis_models import (
    ArbitrationCourtPreviewTable, BankruptcyPreviewTable,
    BankruptcyFullTable, CorruptionPreviewTable, CorruptionFullTable,
    CourtGeneralJurPreviewTable, CourtGeneralJurCategoricalTable,
    PledgesPreviewTable, PledgeFullTable, PledgePartiesTable, PledgeObjectTable,
    DisqualifiedPersonFullTable,
    FSSPPreviewTable, FSSPFullTable, MLIndexFullTable,
    PartInOrgPreviewTable, PartInOrgFullTable, PartInOrgOrganizationTable, PartInOrgIndividualTable, PartInOrgRoleTable,
    TerrorListFullTable, IrbisPerson,
    TaxArrearsFullTable, TaxArrearsFieldTable
)
from server.tasks.base.base import BaseSearchTask
from server.tasks.celery_config import get_event_loop
from server.logger import SearchLogger
from server.api.dao.irbis.match_type import MatchTypeDAO
from server.api.dao.irbis.person_regions import PersonRegionsDAO
from sqlalchemy.ext.asyncio import AsyncSession


class IrbisSearchTask(BaseSearchTask):
    def __init__(self, search_filters: dict):
        super().__init__(search_filters["query_id"], search_filters["price"])
        self.person_uuid = ''
        self.first_name = search_filters["first_name"]
        self.last_name = search_filters["last_name"]
        self.regions = search_filters["regions"]
        self.second_name = search_filters["second_name"]
        self.birth_date = search_filters["birth_date"]
        self.passport_series = search_filters["passport_series"]
        self.passport_number = search_filters["passport_number"]
        self.inn = search_filters["inn"]

        self.person = BaseAuthIRBIS(
            first_name=self.first_name,
            last_name=self.last_name,
            regions=self.regions,
            second_name=self.second_name,
            birth_date=self.birth_date,
            passport_series=self.passport_series,
            passport_number=self.passport_number,
            inn=self.inn,
        )

        self.logger = SearchLogger(self.query_id, 'search_irbis.log')

    async def _process_search(self, db: AsyncSession):
        try:
            # person_uuid = await self.person.get_person_uuid()
            self.person_uuid = 'ae980143-1aef-4426-a81f-c85a2c104dc4'  # 'f1b008d9-5ed1-49f2-8be0-997817a9e48a'
            if self.person_uuid:
                if self.second_name:
                    fullname = f'{self.last_name} {self.first_name} {self.second_name}'
                else:
                    fullname = f'{self.last_name} {self.first_name}'

                person = IrbisPerson(
                    query_id=self.query_id,
                    person_uuid=self.person_uuid,
                    fullname=fullname,
                    birth_date=self.birth_date,
                    passport_series=self.passport_series,
                    passport_number=self.passport_number,
                    inn=self.inn,
                )
                db.add(person)
                await db.flush()
                irbis_person_id = person.id

                await self._arbitration_court_data(irbis_person_id, db),
                await self._bankruptcy_data(irbis_person_id, db),
                await self._corruption_data(irbis_person_id, db),
                await self._court_of_gen_jur_data(irbis_person_id, db),
                await self._pledges_data(irbis_person_id, db),
                await self._disqualified_pers_data(irbis_person_id, db),
                await self._fssp_data(irbis_person_id, db),
                await self._ml_index_data(irbis_person_id, db),
                await self._part_in_org_data(irbis_person_id, db),
                await self._tax_areas_data(irbis_person_id, db),
                await self._terror_list_data(irbis_person_id, db),

                await PersonRegionsDAO.add_regions(irbis_person_id, self.regions, db)
                await db.commit()

        except Exception as e:
            self.logger.log_error(f"Создание записи провалилось. Ошибка: {e}")
            logger.error(f"Создание записи провалилось. Ошибка: {e}")

    async def _update_balances(self, db):
        pass

    async def _arbitration_court_data(self, irbis_person_id: int, db: AsyncSession):
        data_preview_name, data_preview_inn = await ArbitrationCourt.get_data_preview(self.person_uuid)

        arbitr_preview_name = ArbitrationCourtPreviewTable(
            irbis_person_id=irbis_person_id,
            type="name",
            plaintiff=data_preview_name["P"],
            responder=data_preview_name["R"],
        )
        db.add(arbitr_preview_name)

        arbitr_preview_inn = ArbitrationCourtPreviewTable(
            irbis_person_id=irbis_person_id,
            type="inn",
            plaintiff=data_preview_inn["P"],
            responder=data_preview_inn["R"],
        )
        db.add(arbitr_preview_inn)

        arbitration_court_full = []
        for search_type in {'all', 'inn'}:
            found_data = await ArbitrationCourt._process_arbitration_cases(
                irbis_person_id,
                self.person_uuid,
                search_type,
                db,
            )
            arbitration_court_full.extend(found_data)
        db.add_all(arbitration_court_full)

    async def _bankruptcy_data(self, irbis_person_id: int, db: AsyncSession):
        data_preview_name, data_preview_inn = await Bankruptcy.get_data_preview(self.person_uuid)
        full_data_fio = await Bankruptcy.get_full_data(self.person_uuid, 1, 50, 'name')
        full_data_inn = await Bankruptcy.get_full_data(self.person_uuid, 1, 50, 'inn')

        bankruptcy_preview = BankruptcyPreviewTable(
            irbis_person_id=irbis_person_id,
            name=data_preview_name,
            inn=data_preview_inn,
        )
        db.add(bankruptcy_preview)

        # TODO: УДАЛИТЬ ПОСЛЕ РАЗРАБОТКИ АПИ
        temp_result = [
            {
                "category_name": "Физическое лицо",
                "birth_date": "1962-08-30T00:00:00+0100",
                "born_place": "с. Алтуд Прохладненского р-на Кабардино-Балкарской АССР",
                "inn": "071606963648",
                "link": "http://old.bankrot.fedresurs.ru/PrivatePersonCard.aspx?ID=560990BDF93BDF4B9B34996BE1FDBC43&attempt=1",
                "last_name": "Абазехов",
                "uuid": "556fb6ca-5acc-4427-89f1-eec8c84d0f84",
                "second_name": "Часамбиевич",
                "location": "121352, г. Москва, ул. Давыдковская, д. 3, кв. 180",
                "region_name": "г. Москва",
                "id": 395728,
                "first_name": "Хадис",
                "snils": "061-104-972 19",
                "ogrn": 'test',
                "information": 'test',
            },
            {
                "category_name": "Физическое лицо",
                "birth_date": "1978-03-15T00:00:00+0100",
                "born_place": "г. Санкт-Петербург",
                "inn": "781234567890",
                "link": "http://old.bankrot.fedresurs.ru/PrivatePersonCard.aspx?ID=1234567890ABCDEF&attempt=1",
                "last_name": "Иванов",
                "uuid": "123e4567-e89b-12d3-a456-426614174000",
                "second_name": "Петрович",
                "location": "197022, г. Санкт-Петербург, ул. Профессора Попова, д. 5, кв. 12",
                "region_name": "г. Санкт-Петербург",
                "id": 395729,
                "first_name": "Алексей",
                "snils": "123-456-789 01",
                "ogrn": 'test',
                "information": 'test',
            },
            {
                "category_name": "Физическое лицо",
                "birth_date": "1985-11-22T00:00:00+0100",
                "born_place": "г. Екатеринбург",
                "inn": "661122334455",
                "link": "http://old.bankrot.fedresurs.ru/PrivatePersonCard.aspx?ID=ABCDEF1234567890&attempt=1",
                "last_name": "Смирнова",
                "uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "second_name": "Олеговна",
                "location": "620014, г. Екатеринбург, ул. Ленина, д. 24, кв. 45",
                "region_name": "Свердловская область",
                "id": 395730,
                "first_name": "Ольга",
                "snils": "234-567-890 12",
                "ogrn": 'test',
                "information": 'test',
            },
            {
                "category_name": "Физическое лицо",
                "birth_date": "1990-07-08T00:00:00+0100",
                "born_place": "г. Новосибирск",
                "inn": "540987654321",
                "link": "http://old.bankrot.fedresurs.ru/PrivatePersonCard.aspx?ID=0987654321ABCDEF&attempt=1",
                "last_name": "Кузнецов",
                "uuid": "09876543-21ab-cdef-1234-567890abcdef",
                "second_name": "Сергеевич",
                "location": "630099, г. Новосибирск, ул. Советская, д. 15, кв. 7",
                "region_name": "Новосибирская область",
                "id": 395731,
                "first_name": "Дмитрий",
                "snils": "345-678-901 23",
                "ogrn": 'test',
                "information": 'test',
            },
            {
                "category_name": "Физическое лицо",
                "birth_date": "1973-12-01T00:00:00+0100",
                "born_place": "г. Казань",
                "inn": "160123456789",
                "link": "http://old.bankrot.fedresurs.ru/PrivatePersonCard.aspx?ID=1122334455667788&attempt=1",
                "last_name": "Петрова",
                "uuid": "11223344-5566-7788-99aa-bbccddeeff00",
                "second_name": "Ивановна",
                "location": "420111, г. Казань, ул. Баумана, д. 8, кв. 33",
                "region_name": "Республика Татарстан",
                "id": 395732,
                "first_name": "Мария",
                "snils": "456-789-012 34",
                "ogrn": 'test',
                "information": 'test',
            },
        ]
        bankruptcy_full = [
            BankruptcyFullTable(
                irbis_person_id=irbis_person_id,
                first_name=item.get("first_name"),
                second_name=item.get("second_name"),
                last_name=item.get("last_name"),
                birth_date=item.get("birth_date"),
                born_place=item.get("born_place"),
                inn=item.get("inn"),
                ogrn=item.get("ogrn"),
                snils=item.get("snils"),
                old_name=item.get("old_name"),
                category_name=item.get("category_name"),
                location=item.get("location"),
                region_name=item.get("region_name"),
                information=item.get("information"),
                link=item.get("link"),
                search_type='name',
            )
            for item in temp_result  # TODO: Вернуть full_data_fio + full_data_inn
        ]
        db.add_all(bankruptcy_full)

    async def _corruption_data(self, irbis_person_id: int, db: AsyncSession):
        data_preview = await Corruption.get_data_preview(self.person_uuid)
#       full_data = await Corruption.get_full_data(self.person_uuid, 1, 50)

        corruption_preview = CorruptionPreviewTable(
            irbis_person_id=irbis_person_id, 
            count=data_preview,
            )
        db.add(corruption_preview)

        corruption_full = []
        corruption_full = await Corruption._process_corruption_data(
            irbis_person_id, 
            self.person_uuid,
            )
        db.add_all(corruption_full)

        # TODO: УДАЛИТЬ ПОСЛЕ РАЗРАБОТКИ АПИ
        temp_result = [
            {
                "key": "e3a4646f-ef96-471b-86e5-b25562228a97",
                "full_name": "Литонина Ирина Ивановна",
                "organization": "Министерство сельского хозяйства Сахалинской области",
                "position": "Советник департамента экономики и финансов",
                "normative_act": "Пункт 2 части 1 статьи 59.2 Федерального закона от 27 июля 2004 г. № 79-ФЗ \"О государственной гражданской службе Российской Федерации\"",
                "application_date": "2019-10-28",
                "publish_date": "2019-08-07",
                "excluded_reason": "В соответствии с подпунктом \"а\" пункта 15 постановления Правительства Российской Федерации от 5 марта 2018 г. № 228 21 марта 2020 г. сведения подлежат исключению из реестра лиц, уволенных в связи с утратой доверия"
            },
            {
                "key": "a1b2c3d4-5678-90ef-1234-567890abcdef",
                "full_name": "Петров Алексей Владимирович",
                "organization": "Администрация города Краснодара",
                "position": "Начальник отдела имущественных отношений",
                "normative_act": "Пункт 1 части 1 статьи 59.2 Федерального закона от 27 июля 2004 г. № 79-ФЗ \"О государственной гражданской службе Российской Федерации\"",
                "application_date": "2020-03-15",
                "publish_date": "2020-01-20",
                "excluded_reason": "В связи с истечением срока хранения сведений в соответствии с пунктом 16 постановления Правительства Российской Федерации от 5 марта 2018 г. № 228"
            },
            {
                "key": "b2c3d4e5-6789-01fg-2345-678901abcdef",
                "full_name": "Смирнова Ольга Дмитриевна",
                "organization": "Министерство финансов Московской области",
                "position": "Заместитель начальника управления бюджетного планирования",
                "normative_act": "Пункт 3 части 1 статьи 59.2 Федерального закона от 27 июля 2004 г. № 79-ФЗ \"О государственной гражданской службе Российской Федерации\"",
                "application_date": "2021-06-10",
                "publish_date": "2021-04-12",
                "excluded_reason": "На основании решения суда о восстановлении на службе от 15 мая 2022 г."
            },
            {
                "key": "c3d4e5f6-7890-12gh-3456-789012abcdef",
                "full_name": "Кузнецов Денис Сергеевич",
                "organization": "Правительство Нижегородской области",
                "position": "Советник губернатора по экономическим вопросам",
                "normative_act": "Пункт 2 части 1 статьи 59.2 Федерального закона от 27 июля 2004 г. № 79-ФЗ \"О государственной гражданской службе Российской Федерации\"",
                "application_date": "2018-11-05",
                "publish_date": "2018-09-18",
                "excluded_reason": "В связи со смертью гражданского служащего на основании представленных документов"
            },
            {
                "key": "d4e5f6g7-8901-23hi-4567-890123abcdef",
                "full_name": "Волкова Екатерина Александровна",
                "organization": "Министерство здравоохранения Республики Татарстан",
                "position": "Главный специалист отдела кадров",
                "normative_act": "Пункт 1 части 1 статьи 59.2 Федерального закона от 27 июля 2004 г. № 79-ФЗ \"О государственной гражданской службе Российской Федерации\"",
                "application_date": "2022-02-28",
                "publish_date": "2022-01-10",
                "excluded_reason": "В соответствии с подпунктом \"б\" пункта 15 постановления Правительства Российской Федерации от 5 марта 2018 г. № 228 в связи с признанием сведений не соответствующими действительности"
            }
        ]

        corruption_full = [
            CorruptionFullTable(
                irbis_person_id=irbis_person_id,
                full_name=item.get("full_name"),
                organization=item.get("organization"),
                position=item.get("position"),
                normative_act=item.get("normative_act"),
                application_date=item.get("application_date"),
                publish_date=item.get("publish_date"),
                excluded_reason=item.get("excluded_reason"),
            )
            for item in temp_result  # TODO: Вернуть full_data
        ]
        db.add_all(corruption_full)

    async def _court_of_gen_jur_data(self, irbis_person_id: int, db: AsyncSession):
        full_fio_data_preview, short_fio_data_preview = await CourtGeneralJurisdiction.get_data_preview(
            self.person_uuid, "", "all"
        )

        court_gen_preview = []
        for key, item in full_fio_data_preview.items():
            obj = CourtGeneralJurPreviewTable(
                irbis_person_id=irbis_person_id,
                search_type="full",
                court_type=key,
                plan=item.get("plan"),
                deff=item.get("deff"),
                declarant=item.get("declarant"),
                face=item.get("face"),
                lawyer=item.get("lawyer")
            )
            court_gen_preview.append(obj)
        for key, item in short_fio_data_preview.items():
            obj = CourtGeneralJurPreviewTable(
                irbis_person_id=irbis_person_id,
                search_type="short",
                court_type=key,
                plan=item.get("plan"),
                deff=item.get("deff"),
                declarant=item.get("declarant"),
                face=item.get("face"),
                lawyer=item.get("lawyer")
            )
            court_gen_preview.append(obj)
        db.add_all(court_gen_preview)

        category_data = await CourtGeneralJurisdiction.get_category_result(
            self.person_uuid, 'allData', '', 'all'
        )

        court_gen_category = [
            CourtGeneralJurCategoricalTable(
                irbis_person_id=irbis_person_id,
                type=key,
                count=value,
            )
            for key, value in category_data.items()
        ]
        db.add_all(court_gen_category)

        court_gen_full = []
        for match_type_name in {'full', 'partly'}:
            match_type = await MatchTypeDAO.get_type_by_name(match_type_name, db)
            found_data = await CourtGeneralJurisdiction._process_court_cases(
                irbis_person_id,
                self.person_uuid,
                match_type,
                db,
            )
            court_gen_full.extend(found_data)
        db.add_all(court_gen_full)

    async def _pledges_data(self, irbis_person_id: int, db: AsyncSession):
        data_preview = await Pledges.get_data_preview(self.person_uuid)
        full_data = await Pledges.get_full_data(self.person_uuid, 1, 100)

        pledges_preview = [
            PledgesPreviewTable(
                irbis_person_id=irbis_person_id,
                pledge_count=item.get("pledge_count"),
                pledge_type=item.get("pledge_type"),
                response_id=item.get("id")
            )
            for item in data_preview
        ]
        db.add_all(pledges_preview)

        # TODO: УДАЛИТЬ ПОСЛЕ РАЗРАБОТКИ АПИ
        temp_result = [
            {
                "reg_date": "2018-04-03T00:00:00+0200",
                "pledgers": {
                    "peoples": [
                        {
                            "name": "Михаил Васильевич Воронин",
                            "id": 972975,
                            "birth_date": "1969-05-26T00:00:00+0100"
                        }
                    ]
                },
                "pledge_number": "2018-002-172651-117",
                "pledgees": {
                    "orgs": [
                        {
                            "name": "АКЦИОНЕРНОЕ ОБЩЕСТВО \"ВЛАДБИЗНЕСБАНК\"",
                            "id": 1488583
                        }
                    ]
                },
                "pledges": [
                    {
                        "pledge_id_name": "VIN",
                        "id": 9356883,
                        "pledge_type": "Транспортное средство",
                        "pledge_id": "X7LHSRGAN59375885"
                    }
                ],
                "id": 1260975,
                "pledge_type": "Движимое имущество",
                "uuid": "7090b6c9-a3d5-47d7-95b3-ae031950b9ac"
            },
            {
                "reg_date": "2019-06-15T00:00:00+0200",
                "pledgers": {
                    "peoples": [
                        {
                            "name": "Елена Игоревна Петрова",
                            "id": 972976,
                            "birth_date": "1985-12-14T00:00:00+0100"
                        }
                    ]
                },
                "pledge_number": "2019-003-184532-218",
                "pledgees": {
                    "orgs": [
                        {
                            "name": "ПАО \"СБЕРБАНК\"",
                            "id": 1488584
                        }
                    ]
                },
                "pledges": [
                    {
                        "pledge_id_name": "VIN",
                        "id": 9356884,
                        "pledge_type": "Транспортное средство",
                        "pledge_id": "Z94CB41BAGR323004"
                    }
                ],
                "id": 1260976,
                "pledge_type": "Движимое имущество",
                "uuid": "8191c7da-b4e6-58e8-06c4-bf142061cad0"
            },
            {
                "reg_date": "2020-02-28T00:00:00+0200",
                "pledgers": {
                    "peoples": [
                        {
                            "name": "Алексей Дмитриевич Смирнов",
                            "id": 972977,
                            "birth_date": "1978-03-22T00:00:00+0100"
                        }
                    ]
                },
                "pledge_number": "2020-001-195743-319",
                "pledgees": {
                    "orgs": [
                        {
                            "name": "АО \"АЛЬФА-БАНК\"",
                            "id": 1488585
                        }
                    ]
                },
                "pledges": [
                    {
                        "pledge_id_name": "VIN",
                        "id": 9356885,
                        "pledge_type": "Транспортное средство",
                        "pledge_id": "XW8ZZZ61ZJG260432"
                    }
                ],
                "id": 1260977,
                "pledge_type": "Движимое имущество",
                "uuid": "92a2d8eb-c5f7-69f9-17d5-ce253172dbe1"
            },
            {
                "reg_date": "2021-08-12T00:00:00+0200",
                "pledgers": {
                    "peoples": [
                        {
                            "name": "Ольга Сергеевна Козлова",
                            "id": 972978,
                            "birth_date": "1992-07-08T00:00:00+0100"
                        }
                    ]
                },
                "pledge_number": "2021-004-206854-420",
                "pledgees": {
                    "orgs": [
                        {
                            "name": "ПАО \"ВТБ\"",
                            "id": 1488586
                        }
                    ]
                },
                "pledges": [
                    {
                        "pledge_id_name": "VIN",
                        "id": 9356886,
                        "pledge_type": "Транспортное средство",
                        "pledge_id": "KMHJT81VPFU028765"
                    }
                ],
                "id": 1260978,
                "pledge_type": "Движимое имущество",
                "uuid": "a3b3e9fc-d6g8-70fa-28e6-df364283ecf2"
            },
            {
                "reg_date": "2022-11-05T00:00:00+0200",
                "pledgers": {
                    "peoples": [
                        {
                            "name": "Денис Владимирович Никитин",
                            "id": 972979,
                            "birth_date": "1983-09-30T00:00:00+0100"
                        }
                    ]
                },
                "pledge_number": "2022-005-217965-521",
                "pledgees": {
                    "orgs": [
                        {
                            "name": "АО \"РОССЕЛЬХОЗБАНК\"",
                            "id": 1488587
                        }
                    ]
                },
                "pledges": [
                    {
                        "pledge_id_name": "VIN",
                        "id": 9356887,
                        "pledge_type": "Транспортное средство",
                        "pledge_id": "WAUZZZ8K9NA012345"
                    }
                ],
                "id": 1260979,
                "pledge_type": "Движимое имущество",
                "uuid": "b4c4f0gd-e7h9-81gb-39f7-eg475394fdg3"
            }
        ]

        pledges_full = []
        for pledge_info in temp_result:  # TODO: Вернуть full_data:
            all_pledge_parties = []
            for pledge_type in {'pledgers', 'pledgees'}:
                info = pledge_info.get(pledge_type)
                if info:
                    for role_type in {'orgs', 'peoples'}:
                        parties = [
                            PledgePartiesTable(
                                name=party.get("name", ""),
                                type=pledge_type,
                                subtype=role_type,
                                birth_date=party.get("birth_date"),
                                inn=party.get("inn"),
                                ogrn=party.get("ogrn")
                            )
                            for party in info.get(role_type, [])
                        ]
                        all_pledge_parties.extend(parties)

            pledges = [
                PledgeObjectTable(
                    pledge_num_name=pledge.get("pledge_id_name", ""),
                    pledge_num=pledge.get("pledge_id", ""),
                    pledge_type=pledge.get("pledge_type", ""),
                )
                for pledge in pledge_info.get("pledges", [])
            ]

            obj = PledgeFullTable(
                irbis_person_id=irbis_person_id,
                reg_date=pledge_info.get('reg_date'),
                pledge_reestr_number=pledge_info.get('pledge_number'),
                pledge_type=pledge_info.get("pledge_type"),
                parties=all_pledge_parties,
                pledges=pledges,
            )
            pledges_full.append(obj)
        db.add_all(pledges_full)

    async def _disqualified_pers_data(self, irbis_person_id: int, db: AsyncSession):
        full_data = await DisqualifiedPersons.get_full_data(self.person_uuid, 1, 50)

        # TODO: УДАЛИТЬ ПОСЛЕ РАЗРАБОТКИ АПИ
        temp_result = [
            {
                "start_date_disq": "2018-09-25T00:00:00+0200",
                "reestr_key": "194000029739",
                "birth_date": "1984-08-02T00:00:00+0200",
                "office": "ДИРЕКТОР",
                "fio": "АБАКУМОВ АНДРЕЙ ВЛАДИМИРОВИЧ",
                "article": "Ч.5 СТ. 14.25 КОАП РФ",
                "end_date_disq": "2019-09-24T00:00:00+0200",
                "bornplace": "РОССИЯ, Г. ТОЛЬЯТТИ САМАРСКАЯ ОБЛ.",
                "fio_judge": "БУКОВСКИЙ Р Г",
                "office_judge": "МИРОВОЙ СУДЬЯ",
                "id": 20298,
                "legal_name": "ООО \"ТРАНСГРУПП\"",
                "department": "ИФНС ПО КАЛУЖСКОЙ ОБЛАСТИ",
            },
            {
                "start_date_disq": "2020-01-15T00:00:00+0200",
                "reestr_key": "195000045621",
                "birth_date": "1979-03-12T00:00:00+0200",
                "office": "ГЛАВНЫЙ БУХГАЛТЕР",
                "fio": "ПЕТРОВА ЕЛЕНА ИГОРЕВНА",
                "article": "Ч.3 СТ. 14.25 КОАП РФ",
                "end_date_disq": "2022-01-14T00:00:00+0200",
                "bornplace": "РОССИЯ, Г. МОСКВА",
                "fio_judge": "ИВАНОВА М С",
                "office_judge": "МИРОВОЙ СУДЬЯ",
                "id": 20299,
                "legal_name": "ООО \"ФИНАНСЫ И КРЕДИТ\"",
                "department": "ИФНС ПО Г. МОСКВЕ",
            },
            {
                "start_date_disq": "2019-05-10T00:00:00+0200",
                "reestr_key": "193000038492",
                "birth_date": "1988-11-25T00:00:00+0200",
                "office": "ИСПОЛНИТЕЛЬНЫЙ ДИРЕКТОР",
                "fio": "СИДОРОВ ДМИТРИЙ АЛЕКСАНДРОВИЧ",
                "article": "Ч.4 СТ. 14.25 КОАП РФ",
                "end_date_disq": "2021-05-09T00:00:00+0200",
                "bornplace": "РОССИЯ, Г. САНКТ-ПЕТЕРБУРГ",
                "fio_judge": "ПЕТРОВ А В",
                "office_judge": "АРБИТРАЖНЫЙ СУДЬЯ",
                "id": 20300,
                "legal_name": "ЗАО \"СТРОЙИНВЕСТ\"",
                "department": "ИФНС ПО САНКТ-ПЕТЕРБУРГУ",
            },
            {
                "start_date_disq": "2021-03-08T00:00:00+0200",
                "reestr_key": "196000052783",
                "birth_date": "1991-07-18T00:00:00+0200",
                "office": "КОММЕРЧЕСКИЙ ДИРЕКТОР",
                "fio": "КОЗЛОВА АНАСТАСИЯ СЕРГЕЕВНА",
                "article": "Ч.2 СТ. 14.25 КОАП РФ",
                "end_date_disq": "2023-03-07T00:00:00+0200",
                "bornplace": "РОССИЯ, Г. ЕКАТЕРИНБУРГ СВЕРДЛОВСКАЯ ОБЛ.",
                "fio_judge": "СМИРНОВ К Д",
                "office_judge": "МИРОВОЙ СУДЬЯ",
                "id": 20301,
                "legal_name": "ООО \"УРАЛПРОМТОРГ\"",
                "department": "ИФНС ПО СВЕРДЛОВСКОЙ ОБЛАСТИ",
            },
            {
                "start_date_disq": "2022-07-20T00:00:00+0200",
                "reestr_key": "197000061894",
                "birth_date": "1982-12-05T00:00:00+0200",
                "office": "ГЕНЕРАЛЬНЫЙ ДИРЕКТОР",
                "fio": "НИКИТИН ИВАН ВАСИЛЬЕВИЧ",
                "article": "Ч.5 СТ. 14.25 КОАП РФ",
                "end_date_disq": "2024-07-19T00:00:00+0200",
                "bornplace": "РОССИЯ, Г. НОВОСИБИРСК НОВОСИБИРСКАЯ ОБЛ.",
                "fio_judge": "ФЕДОРОВА О Л",
                "office_judge": "АРБИТРАЖНЫЙ СУДЬЯ",
                "id": 20302,
                "legal_name": "АО \"СИБИРСКИЕ ТЕХНОЛОГИИ\"",
                "department": "ИФНС ПО НОВОСИБИРСКОЙ ОБЛАСТИ",
            }
        ]

        disqualified_full = [
            DisqualifiedPersonFullTable(
                irbis_person_id=irbis_person_id,
                birth_date=item.get("birth_date"),
                fio=item.get("fio"),
                article=item.get("article"),
                start_date_disq=item.get("start_date_disq"),
                end_date_disq=item.get("end_date_disq"),
                bornplace=item.get("bornplace"),
                fio_judge=item.get("fio_judge"),
                office_judge=item.get("office_judge"),
                legal_name=item.get("legal_name"),
                office=item.get("office"),
                department=item.get("department"),
            )
            for item in temp_result  # TODO: Вернуть full_data
        ]
        db.add_all(disqualified_full)

    async def _fssp_data(self, irbis_person_id: int, db: AsyncSession):
        data_preview = await FSSP.get_data_preview(self.person_uuid)
        data_full = await FSSP.get_full_data(self.person_uuid, 1, 50)

        fssp_preview = [
            FSSPPreviewTable(
                irbis_person_id=irbis_person_id,
                response_id=item.get("id"),
                type=item.get("type"),
                type_sum=item.get("type_sum"),
                type_count=item.get("type_count")
            )
            for item in data_preview
        ]
        db.add_all(fssp_preview)

        fssp_full = [
            FSSPFullTable(
                irbis_person_id=irbis_person_id,
                ip=item.get("ip"),
                fio=item.get("fio"),
                rosp=item.get("rosp"),
                type_ip=item.get("type_ip"),
                summ=item.get("summ"),
                rekv=item.get("rekv"),
                end_cause=item.get("end_cause"),
                pristav=item.get("pristav"),
                pristav_phones=item.get("pristav_phones"),
            )
            for item in data_full
        ]
        db.add_all(fssp_full)

    async def _ml_index_data(self, irbis_person_id: int, db: AsyncSession):
        full_data = await MLIndex.get_full_data(self.person_uuid)
        mlindex_full = MLIndexFullTable(
            irbis_person_id=irbis_person_id,
            scoring=full_data.get("scoring", 0),
            errors="\n".join(full_data.get("errors", [])),
            progress=full_data.get("progress", 0),
            popularity_full=full_data.get("popularity", dict()).get("full", 0),
            popularity_short=full_data.get("popularity", dict()).get("short", 0),
        )
        db.add(mlindex_full)

    async def _part_in_org_data(self, irbis_person_id: int, db: AsyncSession):
        data_preview_all, data_preview_selected = await ParticipationOrganization.get_data_preview(self.person_uuid)
        full_data = await ParticipationOrganization.get_full_data(self.person_uuid, 1, 50, 'all')

        part_in_org_preview = []
        for item in data_preview_all:
            obj = PartInOrgPreviewTable(
                irbis_person_id=irbis_person_id,
                filter_type="all",
                count=item.get("count"),
                part_type=item.get("type"),
            )
            part_in_org_preview.append(obj)
        for item in data_preview_selected:
            obj = PartInOrgPreviewTable(
                irbis_person_id=irbis_person_id,
                filter_type="selected",
                count=item.get("count"),
                part_type=item.get("type"),
            )
            part_in_org_preview.append(obj)
        db.add_all(part_in_org_preview)

        part_in_org_full = []
        for entry in full_data:
            org_data = entry.get("org_data")
            org_obj = None
            if org_data:
                address: dict = org_data.get('address_obj')
                region_id = None
                full_address = None

                if address:
                    region_id = int(address.get('region_code'))
                    full_address = address.get('full_address')

                okved = org_data.get('okved')
                okved_name = None
                if okved:
                    okved_name = okved.get('name')

                org_obj = PartInOrgOrganizationTable(
                    name=org_data.get("name", ""),
                    inn=org_data.get("inn", ""),
                    ogrn=org_data.get("ogrn"),
                    address=full_address,
                    okved=okved_name,
                    region_id=region_id,
                )

            individual_data = entry.get("individual_data")
            individual_obj = None
            if individual_data:
                roles_data = individual_data.get("roles", [])
                roles_objs = [
                    PartInOrgRoleTable(
                        name=role.get("name", ""),
                        active=role.get("active", False),
                    )
                    for role in roles_data
                ]

                individual_obj = PartInOrgIndividualTable(
                    name=individual_data.get("name", ""),
                    inn=individual_data.get("inn", ""),
                    roles=roles_objs,
                )

            obj = PartInOrgFullTable(
                irbis_person_id=irbis_person_id,
                org=org_obj,
                individual=individual_obj,
            )

            part_in_org_full.append(obj)
        db.add_all(part_in_org_full)

    async def _tax_areas_data(self, irbis_person_id: int, db: AsyncSession):
        full_data = await TaxArrears.get_full_data(self.person_uuid)

        tax_areas_full = []
        for arrear_data in full_data:

            provider = arrear_data.get("provider", "")
            money = arrear_data.get("money", {})
            currency = money.get("currency", {})

            money_name = currency.get("name", "")
            money_value = money.get("value", 0.0)

            arrear_obj = TaxArrearsFullTable(
                irbis_person_id=irbis_person_id,
                provider=provider,
                money_name=money_name,
                money_value=money_value,
            )

            info_fields = arrear_data.get("infoFields", [])
            for field in info_fields:
                field_obj = TaxArrearsFieldTable(
                    type="info",
                    field_name=field.get("name", ""),
                    value=field.get("value", ""),
                    tax_arrear=arrear_obj,
                )
                arrear_obj.fields.append(field_obj)

            payment_fields = arrear_data.get("paymentFields", [])
            for field in payment_fields:
                field_obj = TaxArrearsFieldTable(
                    type="payment",
                    field_name=field.get("name", ""),
                    value=field.get("value", ""),
                    tax_arrear=arrear_obj,
                )
                arrear_obj.fields.append(field_obj)

            tax_areas_full.append(arrear_obj)
        db.add_all(tax_areas_full)

    async def _terror_list_data(self, irbis_person_id: int, db: AsyncSession):
        full_data = await TerrorList.get_full_data(self.person_uuid, 1, 50)

        # TODO: УДАЛИТЬ ПОСЛЕ РАЗРАБОТКИ АПИ
        temp_result = [
            {
                "birth_place": "Г. СЕВЕРСК ТОМСКАЯ ОБЛАСТЬ",
                "id": 3759712,
                "fio": "ТЮМЕНЦЕВ ВАДИМ ВИКТОРОВИЧ",
                "birth_date": "1980-12-03T00:00:00+0100"
            }
        ]

        terror_list_full = [
            TerrorListFullTable(
                irbis_person_id=irbis_person_id,
                fio=item.get("fio"),
                birth_date=item.get("birth_date"),
                birth_place=item.get("birth_place"),
            )
            for item in temp_result  # TODO: Вернуть full_data
        ]
        db.add_all(terror_list_full)


@shared_task(bind=True, acks_late=True, queue='irbis_tasks')
def start_search_by_irbis(self, search_filters: dict):
    loop = get_event_loop()
    task = IrbisSearchTask(search_filters)
    loop.run_until_complete(task.execute())
