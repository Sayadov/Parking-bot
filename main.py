import os
from dotenv import load_dotenv

from packages.drivers.s3_driver import S3Driver
from packages.adapters.s3_adapter import S3Adapter
from packages.entites import State, User, Place
from packages.use_cases.add_place import AddPlaceUseCase
from packages.use_cases.set_place import SetPlaceUseCase
from packages.use_cases.delete_place import DeletePlaceUseCase

load_dotenv()

endpoint_url = os.getenv("ENDPOINT_URL")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
bucket = os.getenv("BUCKET")
key = os.getenv("KEY")

s3_driver = S3Driver(
    endpoint_url=endpoint_url,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)
s3_adapter = S3Adapter(s3_driver=s3_driver, bucket=bucket, key=key)
add_place_use_case = AddPlaceUseCase(s3_adapter=s3_adapter)
set_place_use_case = SetPlaceUseCase(s3_adapter=s3_adapter)
delete_place_use_case = DeletePlaceUseCase(s3_adapter=s3_adapter)


def init_new_state():
    state = State(users=[User(id=1)], places=[Place(id=2)])
    s3_adapter.upload(state=state)


init_new_state()
add_place_use_case.execute(Place(id=123))
set_place_use_case.execute(Place(id=123))
delete_place_use_case.execute(Place(id=123))
set_place_use_case.execute(Place(id=123))
