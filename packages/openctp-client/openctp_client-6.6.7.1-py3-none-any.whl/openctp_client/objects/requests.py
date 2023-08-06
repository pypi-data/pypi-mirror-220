from pydantic import BaseModel
from .enums import CtpMethod
from .fields import *


class CtpRequest(BaseModel):
    method: CtpMethod
    
    @property
    def args(self) -> list[any]:
        return []
