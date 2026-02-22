import botocore

from packages.ports import IS3Adapter, IS3Driver
from packages.entites import State
from packages.errors import StorageConflictError


class S3Adapter(IS3Adapter):
    def __init__(self, s3_driver: IS3Driver, bucket: str, key: str):
        self._driver = s3_driver
        self.bucket = bucket
        self.key = key
        self._last_etag = None

    def download(self) -> State:
        try:
            res = self._driver.get_object(self.bucket, self.key)
            self._last_etag = res["ETag"]
            return State.model_validate_json(res["Body"].read())
        except Exception as ex:
            raise ex

    def upload(self, state: State):
        try:
            self._driver.put_object(
                self.bucket, self.key, state.model_dump_json(), self._last_etag
            )
        except botocore.exceptions.ClientError as ex:
            if ex.response["Error"]["Code"] in ["PreconditionFailed", "412"]:
                raise StorageConflictError()
            raise ex
