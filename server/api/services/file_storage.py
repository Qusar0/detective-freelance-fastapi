# server/api/services/file_storage.py
import os
from datetime import datetime
from pathlib import Path
from fastapi import HTTPException
import logging

class FileStorageService:
    def __init__(self, storage_root: str = "query_data"):
        self.storage_root = Path(storage_root)
        self.storage_root.mkdir(parents=True, exist_ok=True)
    
    async def save_query_data(self, query_id: int, data: str) -> str:
        try:
            today = datetime.now()
            file_path = self.storage_root / str(today.year) / f"{today.month:02d}" / f"{today.day:02d}"
            file_path.mkdir(parents=True, exist_ok=True)
            
            filename = f"query_{query_id}.txt"
            full_path = file_path / filename
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(data)
            
            return str(full_path)
        except Exception as e:
            logging.error(f"Failed to save query data to file: {e}")
            raise HTTPException(status_code=500, detail="Failed to save query data")

    async def get_query_data(self, file_path: str) -> str:
        try:
            path = Path(file_path)
            if not path.exists():
                raise HTTPException(status_code=404, detail="Query data file not found")
            
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logging.error(f"Failed to read query data from file: {e}")
            raise HTTPException(status_code=500, detail="Failed to read query data")

    async def delete_query_data(self, file_path: str) -> None:
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
        except Exception as e:
            logging.error(f"Failed to delete query data file: {e}")
            raise HTTPException(status_code=500, detail="Failed to delete query data")