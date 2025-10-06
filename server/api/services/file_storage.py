from loguru import logger
import aiofiles
from pathlib import Path
from fastapi import HTTPException


class FileStorageService:
    def __init__(self, storage_root: str = "query_data"):
        self.storage_root = Path(storage_root)
        self.storage_root.mkdir(parents=True, exist_ok=True)

    async def save_query_data(self, query_id: int, data: str) -> str:
        try:
            file_path = self.storage_root / f"query_{query_id}.txt"
            async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
                await f.write(data)
            return str(file_path)
        except Exception as e:
            logger.error(f"Не удалось сохранить данные очереди в файл: {e}")
            raise HTTPException(status_code=500, detail="Failed to save query data")

    @staticmethod
    async def get_query_data(file_path: str) -> str:
        try:
            path = Path(file_path)
            if not path.exists():
                raise HTTPException(status_code=404, detail="Query data file not found")
            async with aiofiles.open(path, 'r', encoding='utf-8') as f:
                return await f.read()
        except Exception as e:
            logger.error(f"Не удалось прочитать данные очереди из файла: {e}")
            raise HTTPException(status_code=500, detail="Failed to read query data")

    @staticmethod
    async def delete_query_data(file_path: str) -> None:
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
        except Exception as e:
            logger.error(f"Не удалось удалить файл с данными очереди: {e}")
            raise HTTPException(status_code=500, detail="Failed to delete query data")


def get_file_storage() -> FileStorageService:
    return FileStorageService()
