from pydantic import BaseModel

class KrBaseModel(BaseModel):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.__post_init__()

    def __post_init__(self):
        pass
