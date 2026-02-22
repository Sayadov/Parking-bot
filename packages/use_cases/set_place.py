import pytz
from datetime import datetime

from packages.ports import IS3Adapter
from packages.entites import Place
from packages.errors import StorageConflictError, PlaceBookedToday, PlaceNotFound

current_tz = pytz.timezone("Asia/Novosibirsk")


class SetPlaceUseCase:
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
                if target_place.is_booked_today:
                    raise PlaceBookedToday("Уже занято")
                target_place.date_set = datetime.now(current_tz).date()
                self._s3_adapter.upload(state=state)
                return
            except StorageConflictError:
                continue
            except Exception as ex:
                raise ex
