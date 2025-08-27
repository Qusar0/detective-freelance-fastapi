from celery import shared_task
from loguru import logger
from server.api.IRBIS_parser.arbitration_court import ArbitrationCourt
from server.api.IRBIS_parser.bankruptcy import Bankruptcy
from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS
from server.api.IRBIS_parser.corruption import Corruption
from server.api.IRBIS_parser.court_of_general_jurisdiction import CourtGeneralJurisdiction
from server.api.IRBIS_parser.deposits import Deposits
from server.api.IRBIS_parser.disqualified_persons import DisqualifiedPersons
from server.api.IRBIS_parser.fssp import FSSP
from server.api.IRBIS_parser.ml_index import MLIndex
from server.api.IRBIS_parser.participation_in_organization import ParticipationOrganization
from server.api.IRBIS_parser.tax_arrears import TaxArrears
from server.api.IRBIS_parser.terror_list import TerrorList
from server.api.models.irbis_models import (
    ArbitrationCourtPreviewTable, ArbitrationCourtFullTable, BankruptcyPreviewTable,
    BankruptcyFullTable, CorruptionPreviewTable, CorruptionFullTable,
    CourtGeneralJurPreviewTable, CourtGeneralJurCategoricalTable,
    DepositsPreviewTable, DepositsFullTable, DepositsPartiesTable, DepositsPledgeObjectTable,
    DisqualifiedPersonFullTable,
    FSSPPreviewTable, FSSPFullTable, MLIndexFullTable,
    PartInOrgPreviewTable, PartInOrgFullTable, PartInOrgOrgTable, PartInOrgIndividualTable, PartInOrgRoleTable,
    TerrorListFullTable, IrbisPerson,
    TaxArrearsFullTable, TaxArrearsFieldTable
)
from server.tasks.base.base import BaseSearchTask
from server.tasks.celery_config import get_event_loop
from server.tasks.logger import SearchLogger
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
            self.person_uuid = 'f1b008d9-5ed1-49f2-8be0-997817a9e48a'
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
                await self._deposits_data(irbis_person_id, db),
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
        full_data = await ArbitrationCourt.get_full_data(self.person_uuid, 1, 50, 'all')

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

        arbitr_full = []
        for item in full_data:
            obj = ArbitrationCourtFullTable(
                irbis_person_id=irbis_person_id,
                court_name_val=item.get("court_name_val", None),
                role=item.get("role", None),
                case_date=item.get("case_date", None),
                case_id=item.get("case_id", None),
                inn=item.get("inn", None),
                name=item.get("name", None),
                case_type=item.get("case_type", None),
                response_id=item.get("id", None),
                address_val=item.get("address_val", None)
            )
            arbitr_full.append(obj)
        db.add_all(arbitr_full)

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
                link=item.get("link")
            )
            for item in full_data_fio + full_data_inn
        ]
        db.add_all(bankruptcy_full)

    async def _corruption_data(self, irbis_person_id: int, db: AsyncSession):
        data_preview = await Corruption.get_data_preview(self.person_uuid)
        full_data = await Corruption.get_full_data(self.person_uuid, 1, 50)

        corruption_preview = CorruptionPreviewTable(irbis_person_id=irbis_person_id, count=data_preview)
        db.add(corruption_preview)

        corruption_full = [
            CorruptionFullTable(
                irbis_person_id=irbis_person_id,
                key=item.get("key"),
                full_name=item.get("full_name"),
                organization=item.get("organization"),
                position=item.get("position"),
                normative_act=item.get("normative_act"),
                application_date=item.get("application_date"),
                publish_date=item.get("publish_date"),
                excluded_reason=item.get("excluded_reason"),
            )
            for item in full_data
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

    async def _deposits_data(self, irbis_person_id: int, db: AsyncSession):
        data_preview = await Deposits.get_data_preview(self.person_uuid)
        full_data = await Deposits.get_full_data(self.person_uuid, 1, 100)

        deposits_preview = [
            DepositsPreviewTable(
                irbis_person_id=irbis_person_id,
                pledge_count=item.get("pledge_count"),
                pledge_type=item.get("pledge_type"),
                response_id=item.get("id")
            )
            for item in data_preview
        ]
        db.add_all(deposits_preview)

        deposits_full = []
        for deposit_info in full_data:
            parties = [
                DepositsPartiesTable(
                    name=party.get("name", ""),
                    external_id=party.get("external_id", 0),
                    type=party.get("type", ""),
                    subtype=party.get("subtype", ""),
                    birth_date=party.get("birth_date", ""),
                    inn=party.get("inn"),
                    ogrn=party.get("ogrn")
                )
                for party in deposit_info.get("parties", [])
            ]

            pledges = [
                DepositsPledgeObjectTable(
                    pledge_id_name=pledge.get("pledge_id_name", ""),
                    pledge_id=pledge.get("pledge_id", ""),
                    pledge_type=pledge.get("pledge_type", ""),
                    external_id=pledge.get("external_id", 0)
                )
                for pledge in deposit_info.get("pledges", [])
            ]

            obj = DepositsFullTable(
                irbis_person_id=irbis_person_id,
                pledge_count=deposit_info.get("pledge_count", 0),
                pledge_type=deposit_info.get("pledge_type", ""),
                response_id=deposit_info.get("response_id", 0),
                parties=parties,
                pledges=pledges,
            )
            deposits_full.append(obj)
        db.add_all(deposits_full)

    async def _disqualified_pers_data(self, irbis_person_id: int, db: AsyncSession):
        full_data = await DisqualifiedPersons.get_full_data(self.person_uuid, 1, 50)

        disqualified_full = [
            DisqualifiedPersonFullTable(
                irbis_person_id=irbis_person_id,
                response_id=item.get("id"),
                reestr_key=item.get("reestr_key"),
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
            for item in full_data
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
                response_id=item.get("id")
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
                org_obj = PartInOrgOrgTable(
                    name=org_data.get("name", ""),
                    inn=org_data.get("inn", ""),
                    ogrn=org_data.get("ogrn"),
                    adress=org_data.get("adress", ""),
                    okved=org_data.get("okved"),
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
                filter_type=entry.get("filter_type", ""),
                count=entry.get("count", 0),
                part_type=entry.get("part_type", ""),
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
            money_code = currency.get("code", 0)
            money_value = money.get("value", 0.0)

            arrear_obj = TaxArrearsFullTable(
                irbis_person_id=irbis_person_id,
                provider=provider,
                money_name=money_name,
                money_code=money_code,
                money_value=money_value,
            )

            info_fields = arrear_data.get("infoFields", [])
            for field in info_fields:
                field_obj = TaxArrearsFieldTable(
                    type="info",
                    field_id=field.get("id", ""),
                    field_name=field.get("name", ""),
                    field_type=field.get("fieldType", ""),
                    value=field.get("value", ""),
                    arrear=arrear_obj,
                )
                arrear_obj.fields.append(field_obj)

            payment_fields = arrear_data.get("paymentFields", [])
            for field in payment_fields:
                field_obj = TaxArrearsFieldTable(
                    type="payment",
                    field_id=field.get("id", ""),
                    field_name=field.get("name", ""),
                    field_type=field.get("fieldType", ""),
                    value=field.get("value", ""),
                    arrear=arrear_obj,
                )
                arrear_obj.fields.append(field_obj)

            tax_areas_full.append(arrear_obj)
        db.add_all(tax_areas_full)

    async def _terror_list_data(self, irbis_person_id: int, db: AsyncSession):
        full_data = await TerrorList.get_full_data(self.person_uuid, 1, 50)
        terror_list_full = [
            TerrorListFullTable(
                irbis_person_id=irbis_person_id,
                response_id=item.get("id"),
                fio=item.get("fio"),
                birth_date=item.get("birth_date"),
                birth_place=item.get("birth_place"),
            )
            for item in full_data
        ]
        db.add_all(terror_list_full)


@shared_task(bind=True, acks_late=True, queue='irbis_tasks')
def start_search_by_irbis(self, search_filters: dict):
    loop = get_event_loop()
    task = IrbisSearchTask(search_filters)
    loop.run_until_complete(task.execute())
