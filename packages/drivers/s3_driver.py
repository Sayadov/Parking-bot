import boto3

from packages.ports import IS3Driver


class S3Driver(IS3Driver):
    def __init__(
        self, endpoint_url: str, aws_access_key_id: str, aws_secret_access_key: str
    ):
        self.session = boto3.session.Session()
        self.client = self.session.client(
            service_name="s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    def get_object(self, bucket: str, key: str):
        return self.client.get_object(Bucket=bucket, Key=key)

    def put_object(self, bucket: str, key: str, body: str, etag: str = None):
        params = {"Bucket": bucket, "Key": key, "Body": body}
        if etag:
            params["IfMatch"] = etag
        return self.client.put_object(**params)
