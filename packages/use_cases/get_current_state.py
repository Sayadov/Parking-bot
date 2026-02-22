from packages.ports import IS3Adapter


class GetCurrentState:
    def __init__(self, s3: IS3Adapter):
        self._s3 = s3

    def execute(self):
        return self._s3.download()
