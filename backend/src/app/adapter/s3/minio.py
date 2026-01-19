import io
from collections.abc import AsyncIterable

import botocore
from types_aiobotocore_s3.client import S3Client


class MinIOClient:
    def __init__(
            self,
            client: S3Client,
    ) -> None:
        self.client = client

    async def get_object(
            self,
            bucket: str,
            key: str,
    ) -> AsyncIterable[bytes]:
        response = await self.client.get_object(
            Bucket=bucket,
            Key=key,
        )
        async with response["Body"] as stream:
            async for chunk in stream.content.iter_chunked(60 * 1024 * 1024):
                yield chunk

    async def put_object(
            self,
            bucket: str,
            key: str,
            file: io.BytesIO | str | bytes,
    ) -> None:
        await self.client.put_object(
            Bucket=bucket,
            Key=key,
            Body=file,
        )

    async def delete_object(
            self,
            bucket: str,
            key: str,
    ) -> None:
        try:
            await self.client.delete_object(
                Bucket=bucket,
                Key=key,
            )
        except botocore.exceptions.ClientError:
            pass

    async def copy_object(
            self,
            bucket: str,
            old_key: str,
            new_key: str,
    ) -> None:
        try:
            await self.client.copy_object(
                Bucket=bucket,
                CopySource={
                    "Bucket": bucket,
                    "Key": old_key,
                },
                Key=new_key,
            )
        except botocore.exceptions.ClientError:
            pass
