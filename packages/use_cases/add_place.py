import pytz
from datetime import datetime, timedelta

from packages.ports import IS3Adapter
from packages.entites import Place, State
from packages.errors import StorageConflictError, PlaceExist


current_tz = pytz.timezone("Asia/Novosibirsk")


class AddPlaceUseCase:
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

                if target_place:
                    raise PlaceExist("Место уже существует")
                place.date_set = (datetime.now(current_tz) - timedelta(days=1)).date()
                state.places.append(place)
                self._s3_adapter.upload(state=state)
                return
            except StorageConflictError:
                continue
            except Exception as ex:
                raise ex
