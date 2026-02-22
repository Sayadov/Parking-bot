import pytz
from datetime import datetime, timedelta

from packages.ports import IS3Adapter
from packages.entites import Place
from packages.errors import StorageConflictError, PlaceNotFound

current_tz = pytz.timezone("Asia/Novosibirsk")


class DeletePlaceUseCase:
    def __init__(self, s3_adapter: IS3Adapter):
        self._s3_adapter = s3_adapter

    def execute(
        self,
        place: Place,
    ):
        for _ in range(3):
            try:
                state = self._s3_adapter.download()
                target_place = next(
                    filter(lambda x: x.id == place.id, state.places), None
                )

                if not target_place:
                    raise PlaceNotFound("Место не найдено")
                state.places = [i for i in state.places if i.id != place.id]
                self._s3_adapter.upload(state=state)
                return
            except StorageConflictError:
                continue
            except Exception as ex:
                raise ex
