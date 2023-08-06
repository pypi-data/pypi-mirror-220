from pydantic import BaseModel

class KrBaseModel(BaseModel):
    class Config:
        extra = 'allow'
        underscore_attrs_are_private = True

    def __init__(self, **kw):
        super().__init__(**kw)
        self.__post_init__()

    def __post_init__(self):
        pass
