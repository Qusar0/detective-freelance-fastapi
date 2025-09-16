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
    CorruptionPreviewTable, CorruptionFullTable,
    CourtGeneralJurPreviewTable, CourtGeneralJurCategoricalTable,
    PledgesPreviewTable,
    DisqualifiedPersonPreviewTable,
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
from server.api.dao.irbis.region_subjects import RegionSubjectDAO
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

        bankruptcy_preview = BankruptcyPreviewTable(
            irbis_person_id=irbis_person_id,
            name=data_preview_name,
            inn=data_preview_inn,
        )
        db.add(bankruptcy_preview)

        bankruptcy_full = []
        for search_type in {'name', 'inn'}:
            found_data = await Bankruptcy._process_bankruptcy_data(
                irbis_person_id,
                self.person_uuid,
                search_type,
            )
            bankruptcy_full.extend(found_data)
        db.add_all(bankruptcy_full)

    async def _corruption_data(self, irbis_person_id: int, db: AsyncSession):
        data_preview = await Corruption.get_data_preview(self.person_uuid)

        corruption_preview = CorruptionPreviewTable(
            irbis_person_id=irbis_person_id,
            count=data_preview,
        )
        db.add(corruption_preview)

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

        pledges_full = []
        pledges_full.extend(await Pledges._process_pledgess_data(
            irbis_person_id,
            self.person_uuid,
        ))
        db.add_all(pledges_full)

    async def _disqualified_pers_data(self, irbis_person_id: int, db: AsyncSession):
        data_preview_count = await DisqualifiedPersons.get_data_preview(self.person_uuid)

        disq_pers_preview = DisqualifiedPersonPreviewTable(
            irbis_person_id=irbis_person_id,
            count=data_preview_count
        )
        db.add(disq_pers_preview)

        disqualified_pers_full = await DisqualifiedPersons._process_bankruptcy_data(
            irbis_person_id,
            self.person_uuid,
        )
        db.add_all(disqualified_pers_full)

    async def _fssp_data(self, irbis_person_id: int, db: AsyncSession):
        data_preview = await FSSP.get_data_preview(self.person_uuid)
        #data_full = await FSSP.get_full_data(self.person_uuid, 1, 50)

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

        fssp_full = await FSSP._process_fssp_data(
            irbis_person_id,
            self.person_uuid,
        )
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
                    region_code = int(address.get('region_code'))
                    region = await RegionSubjectDAO.get_region_by_code(region_code, db)
                    region_id = region.id if region else None
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
