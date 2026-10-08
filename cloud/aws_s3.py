import boto3
from botocore.exceptions import ClientError
from typing import BinaryIO
from .interfaces import CloudStorageProvider

class AWSS3Provider(CloudStorageProvider):
    """Implementation of CloudStorageProvider for AWS S3."""
    
    def __init__(self, region_name: str, aws_access_key_id: str, aws_secret_access_key: str):
        self.s3_client = boto3.client(
            's3',
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

    async def upload_file(self, bucket: str, path: str, stream: BinaryIO, content_type: str) -> str:
        try:
            self.s3_client.upload_fileobj(
                stream,
                bucket,
                path,
                ExtraArgs={'ContentType': content_type}
            )
            # Standard S3 URL format
            return f"https://{bucket}.s3.amazonaws.com/{path}"
        except ClientError as e:
            raise RuntimeError(f"Failed to upload to S3: {str(e)}")

    async def download_file(self, bucket: str, path: str) -> BinaryIO:
        import io
        stream = io.BytesIO()
        try:
            self.s3_client.download_fileobj(bucket, path, stream)
            stream.seek(0)
            return stream
        except ClientError as e:
            raise RuntimeError(f"Failed to download from S3: {str(e)}")

    async def generate_presigned_url(self, bucket: str, path: str, expiration_seconds: int = 3600) -> str:
        try:
            response = self.s3_client.generate_presigned_url(
                'put_object',
                Params={'Bucket': bucket, 'Key': path},
                ExpiresIn=expiration_seconds
            )
            return response
        except ClientError as e:
            raise RuntimeError(f"Failed to generate S3 presigned URL: {str(e)}")
