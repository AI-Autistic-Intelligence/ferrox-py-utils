from abc import ABC, abstractmethod
from typing import BinaryIO, Optional

class CloudStorageProvider(ABC):
    
    @abstractmethod
    async def upload_file(self, bucket: str, path: str, stream: BinaryIO, content_type: str) -> str:
        """Uploads a file and returns its public URL or path."""
        pass

    @abstractmethod
    async def download_file(self, bucket: str, path: str) -> BinaryIO:
        """Downloads a file as a binary stream."""
        pass

    @abstractmethod
    async def generate_presigned_url(self, bucket: str, path: str, expiration_seconds: int = 3600) -> str:
        """Generates a secure, temporary URL for uploading or downloading directly from the client."""
        pass

class SecretManagerProvider(ABC):
    
    @abstractmethod
    async def get_secret(self, secret_id: str) -> str:
        """Retrieves a secret payload."""
        pass

class TerraformGenerator(ABC):
    
    @abstractmethod
    def generate_vpc(self, name: str, cidr_block: str) -> str:
        """Generates Terraform HCL for a Virtual Private Cloud."""
        pass
        
    @abstractmethod
    def generate_database(self, name: str, engine: str, version: str, instance_class: str) -> str:
        """Generates Terraform HCL for a managed database (RDS/Cloud SQL)."""
        pass
