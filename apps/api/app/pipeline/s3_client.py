import aioboto3
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class S3Client:
    def __init__(self):
        self.endpoint = settings.MINIO_ENDPOINT
        self.access_key = settings.MINIO_ACCESS_KEY
        self.secret_key = settings.MINIO_SECRET_KEY
        self.bucket = settings.MINIO_BUCKET
        self.session = aioboto3.Session()

    def get_client(self):
        return self.session.client(
            's3',
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        )

    async def init_bucket(self):
        async with self.get_client() as client:
            try:
                await client.head_bucket(Bucket=self.bucket)
            except Exception:
                logger.info(f"Bucket {self.bucket} not found. Creating it.")
                await client.create_bucket(Bucket=self.bucket)

    async def upload_file(self, file_path: str, object_name: str):
        await self.init_bucket()
        async with self.get_client() as client:
            await client.upload_file(file_path, self.bucket, object_name)
            logger.info(f"Uploaded {file_path} to s3://{self.bucket}/{object_name}")

    async def download_file(self, object_name: str, file_path: str):
        async with self.get_client() as client:
            await client.download_file(self.bucket, object_name, file_path)
            logger.info(f"Downloaded s3://{self.bucket}/{object_name} to {file_path}")

s3_client = S3Client()
