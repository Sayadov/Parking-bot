from pydantic import BaseModel
from packages.entites.place import Place
from packages.entites.user import User


class State(BaseModel):
    places: list[Place]
    users: list[User]
