import asyncio
import json
from datetime import datetime
import os
from server.api.IRBIS_parser.arbitration_court import ArbitrationCourt
from server.api.IRBIS_parser.bankruptcy import Bankruptcy
from server.api.IRBIS_parser.corruption import Corruption
from server.api.IRBIS_parser.court_of_general_jurisdiction import CourtGeneralJurisdiction
from server.api.IRBIS_parser.deposits import Deposits
from server.api.IRBIS_parser.disqualified_persons import DisqualifiedPersons
from server.api.IRBIS_parser.fssp import FSSP
from server.api.IRBIS_parser.ml_index import MLIndex
from server.api.IRBIS_parser.participation_in_organization import ParticipationOrganization
from server.api.IRBIS_parser.passport_check import PassportCheck
from server.api.IRBIS_parser.tax_arrears import TaxArrears
from server.api.IRBIS_parser.terror_list import TerrorList

class TestLogger:
    def __init__(self, output_dir="test_results"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.start_time = datetime.now()
    
    def get_test_filename(self, test_name):
        """Генерирует имя файла для теста"""
        timestamp = self.start_time.strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.output_dir, f"{test_name}_{timestamp}.json")
    
    def print_and_save(self, test_name, title, data):
        """Печатает результат и сохраняет в файл"""
        # Создаем структуру для сохранения
        result = {
            "test_name": test_name,
            "timestamp": datetime.now().isoformat(),
            "title": title,
            "data": data
        }
        
        # Печать в консоль
        print(f"\n{'='*50}\n{title.upper()}\n{'='*50}")
        print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))
        
        # Сохранение в файл
        filename = self.get_test_filename(test_name)
        mode = 'a' if os.path.exists(filename) else 'w'
        
        with open(filename, mode, encoding='utf-8') as f:
            if mode == 'a':
                f.write('\n')  # Добавляем разделитель между записями
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        return filename

logger = TestLogger()

async def test_arbitration_court():
    test_name = "arbitration_court"
    arbitration_court = ArbitrationCourt()
    preview = await arbitration_court.get_data_preview('f1b008d9-5ed1-49f2-8be0-997817a9e48a')
    logger.print_and_save(test_name, "Arbitration Court Preview", preview)
    
    page = 1
    data = ['test']
    while data:
        data = await arbitration_court.get_full_data('f1b008d9-5ed1-49f2-8be0-997817a9e48a', page, 10, 'all')
        if data:
            logger.print_and_save(test_name, f"Arbitration Court Page {page}", data)
            page += 1

async def test_bankruptcy():
    test_name = "bankruptcy"
    bankruptcy = Bankruptcy()
    preview = await bankruptcy.get_data_preview('f1b008d9-5ed1-49f2-8be0-997817a9e48a')
    logger.print_and_save(test_name, "Bankruptcy Preview", preview)
    
    page = 1
    data = ['test']
    while data:
        data = await bankruptcy.get_full_data('f1b008d9-5ed1-49f2-8be0-997817a9e48a', page, 10, 'all')
        if data:
            logger.print_and_save(test_name, f"Bankruptcy (All) Page {page}", data)
            page += 1

    # Test with 'name' filter
    page = 1
    data = ['test']
    while data:
        data = await bankruptcy.get_full_data('f1b008d9-5ed1-49f2-8be0-997817a9e48a', page, 10, 'name')
        if data:
            logger.print_and_save(test_name, f"Bankruptcy (Name) Page {page}", data)
            page += 1

async def test_corruption():
    test_name = "corruption"
    corruption = Corruption()
    preview = await corruption.get_data_preview('f1b008d9-5ed1-49f2-8be0-997817a9e48a')
    logger.print_and_save(test_name, "Corruption Preview", preview)
    
    page = 1
    data = ['test']
    while data:
        data = await corruption.get_full_data('f1b008d9-5ed1-49f2-8be0-997817a9e48a', page, 10)
        if data:
            logger.print_and_save(test_name, f"Corruption Page {page}", data)
            page += 1

async def test_court_general_jurisdiction():
    test_name = "court_general_jurisdiction"
    court_general_jurisdiction = CourtGeneralJurisdiction()
    preview = await court_general_jurisdiction.get_data_preview('f1b008d9-5ed1-49f2-8be0-997817a9e48a', 'Навальный', 'selected')
    logger.print_and_save(test_name, "Court General Jurisdiction Preview", preview)
    
    category_result = await court_general_jurisdiction.get_category_result('f1b008d9-5ed1-49f2-8be0-997817a9e48a', 'allData', 'иск', 'selected')
    logger.print_and_save(test_name, "Court General Jurisdiction Category Result", category_result)

    page = 1
    data = ['test']
    while data:
        data = await court_general_jurisdiction.get_full_data('f1b008d9-5ed1-49f2-8be0-997817a9e48a', page, 100, 'selected', 'allData', '')
        if data:
            logger.print_and_save(test_name, f"Court General Jurisdiction Page {page}", data)
            page += 1

async def test_deposits():
    test_name = "deposits"
    deposits = Deposits()
    preview = await deposits.get_data_preview('f1b008d9-5ed1-49f2-8be0-997817a9e48a')
    logger.print_and_save(test_name, "Deposits Preview", preview)
    
    page = 1
    data = ['test']
    while data:
        data = await deposits.get_full_data('f1b008d9-5ed1-49f2-8be0-997817a9e48a', page, 10)
        if data:
            logger.print_and_save(test_name, f"Deposits Page {page}", data)
            page += 1

async def test_disqualified_persons():
    test_name = "disqualified_persons"
    disqualified_persons = DisqualifiedPersons()
    preview = await disqualified_persons.get_data_preview('f1b008d9-5ed1-49f2-8be0-997817a9e48a')
    logger.print_and_save(test_name, "Disqualified Persons Preview", preview)
    
    page = 1
    data = ['test']
    while data:
        data = await disqualified_persons.get_full_data('f1b008d9-5ed1-49f2-8be0-997817a9e48a', page, 10)
        if data:
            logger.print_and_save(test_name, f"Disqualified Persons Page {page}", data)
            page += 1

async def test_fssp():
    test_name = "fssp"
    fssp = FSSP()
    preview = await fssp.get_data_preview('f1b008d9-5ed1-49f2-8be0-997817a9e48a')
    logger.print_and_save(test_name, "FSSP Preview", preview)
    
    page = 1
    data = ['test']
    while data:
        data = await fssp.get_full_data('f1b008d9-5ed1-49f2-8be0-997817a9e48a', page, 10)
        if data:
            logger.print_and_save(test_name, f"FSSP Page {page}", data)
            page += 1

async def test_ml_index():
    test_name = "ml_index"
    ml_index = MLIndex()
    data = await ml_index.get_full_data('f1b008d9-5ed1-49f2-8be0-997817a9e48a')
    logger.print_and_save(test_name, "ML Index Data", data)

async def test_participation_organization():
    test_name = "participation_organization"
    participation_organization = ParticipationOrganization()
    preview = await participation_organization.get_data_preview('f1b008d9-5ed1-49f2-8be0-997817a9e48a')
    logger.print_and_save(test_name, "Participation Organization Preview", preview)
    
    page = 1
    data = ['test']
    while data:
        data = await participation_organization.get_full_data('f1b008d9-5ed1-49f2-8be0-997817a9e48a', page, 1, 'selected')
        if data:
            logger.print_and_save(test_name, f"Participation Organization Page {page}", data)
            page += 1

async def test_passport_check():
    test_name = "passport_check"
    passport_check = PassportCheck()
    result = await passport_check.is_valid('f1b008d9-5ed1-49f2-8be0-997817a9e48a')
    logger.print_and_save(test_name, "Passport Check Result", {"is_valid": result})

async def test_tax_arrears():
    test_name = "tax_arrears"
    tax_arrears = TaxArrears()
    data = await tax_arrears.get_full_data('f1b008d9-5ed1-49f2-8be0-997817a9e48a')
    logger.print_and_save(test_name, "Tax Arrears Data", data)

async def test_terror_list():
    test_name = "terror_list"
    terror_list = TerrorList()
    preview = await terror_list.get_data_preview('f1b008d9-5ed1-49f2-8be0-997817a9e48a')
    logger.print_and_save(test_name, "Terror List Preview", preview)
    
    page = 1
    data = ['test']
    while data:
        data = await terror_list.get_full_data('f1b008d9-5ed1-49f2-8be0-997817a9e48a', page, 1)
        if data:
            logger.print_and_save(test_name, f"Terror List Page {page}", data)
            page += 1

async def main():
    tests = [
        test_arbitration_court,
        test_bankruptcy,
        test_corruption,
        test_court_general_jurisdiction,
        test_deposits,
        test_disqualified_persons,
        test_fssp,
        test_ml_index,
        test_participation_organization,
        test_passport_check,
        test_tax_arrears,
        test_terror_list
    ]
    
    for test in tests:
        try:
            print(f"\n{'#'*50}\nStarting test: {test.__name__}\n{'#'*50}")
            await test()
            print(f"\n{'#'*50}\nCompleted test: {test.__name__}\n{'#'*50}")
        except Exception as e:
            error_msg = f"Error in {test.__name__}: {str(e)}"
            print(f"\n{'!'*50}\n{error_msg}\n{'!'*50}")
    
    print(f"\nAll test results saved to directory: {logger.output_dir}")

if __name__ == '__main__':
    asyncio.run(main())