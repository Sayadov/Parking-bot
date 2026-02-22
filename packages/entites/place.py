import pytz
from pydantic import BaseModel
from datetime import datetime

from packages.entites.user import User


current_tz = pytz.timezone("Asia/Novosibirsk")


class Place(BaseModel):
    id: int
    date_set: datetime | None = None
    user: User | None = None

    @property
    def is_booked_today(self) -> bool:
        if self.date_set is None:
            return False
        return self.date_set.date() == datetime.now(current_tz).date()
