from packages.ports import IS3Adapter
from packages.entites import User


class SetAdminsUseCase:
    def __init__(self, s3_adapter: IS3Adapter):
        self._s3_adapter = s3_adapter

    def execute(
        self,
        user: User,
    ):
        for _ in range(3):
            try:
                state = self._s3_adapter.download()
                find_user = next(filter(lambda x: x.id == user.id, state.users), None)
                if find_user:
                    find_user.is_admin = True
                else:
                    user.is_admin = True
                    state.users.append(user)
                self._s3_adapter.upload(state=state)
                return
            except StorageConflictError:
                continue
            except Exception as ex:
                raise ex
