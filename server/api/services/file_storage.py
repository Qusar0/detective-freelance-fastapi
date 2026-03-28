import aioboto3
from botocore.exceptions import ClientError
from loguru import logger
from fastapi import HTTPException
from server.api.conf.config import settings


class FileStorageService:
    def __init__(self, endpoint: str, access_key: str, secret_key: str, bucket: str):
        self.endpoint = endpoint
        self.bucket = bucket
        self._session = aioboto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    async def save_query_data(self, query_id: int, data: str) -> str:
        key = f"query_{query_id}.html"
        try:
            async with self._session.client("s3", endpoint_url=self.endpoint) as client:
                try:
                    await client.create_bucket(Bucket=self.bucket)
                except ClientError as e:
                    if e.response["Error"]["Code"] not in (
                        "BucketAlreadyOwnedByYou",
                        "BucketAlreadyExists",
                    ):
                        raise
                await client.put_object(
                    Bucket=self.bucket,
                    Key=key,
                    Body=data.encode("utf-8"),
                    ContentType="text/plain; charset=utf-8",
                )
            return key
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Не удалось сохранить данные очереди в S3: {e}")
            raise HTTPException(status_code=500, detail="Failed to save query data")

    async def get_query_data(self, s3_key: str) -> str:
        try:
            async with self._session.client("s3", endpoint_url=self.endpoint) as client:
                response = await client.get_object(Bucket=self.bucket, Key=s3_key)
                async with response["Body"] as stream:
                    content = await stream.read()
            return content.decode("utf-8")
        except ClientError as e:
            code = e.response["Error"]["Code"]
            if code in ("NoSuchKey", "404"):
                raise HTTPException(status_code=404, detail="Query data file not found")
            logger.error(f"Не удалось прочитать данные очереди из S3: {e}")
            raise HTTPException(status_code=500, detail="Failed to read query data")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Не удалось прочитать данные очереди из S3: {e}")
            raise HTTPException(status_code=500, detail="Failed to read query data")

    async def delete_query_data(self, s3_key: str) -> None:
        try:
            async with self._session.client("s3", endpoint_url=self.endpoint) as client:
                await client.delete_object(Bucket=self.bucket, Key=s3_key)
        except Exception as e:
            logger.error(f"Не удалось удалить файл с данными очереди из S3: {e}")
            raise HTTPException(status_code=500, detail="Failed to delete query data")


def get_file_storage() -> FileStorageService:
    return FileStorageService(
        endpoint=settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        bucket=settings.minio_bucket,
    )
