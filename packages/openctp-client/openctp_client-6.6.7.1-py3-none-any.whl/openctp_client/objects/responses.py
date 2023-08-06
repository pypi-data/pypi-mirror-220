from pydantic import BaseModel
from .enums import CtpMethod
from .fields import *


class CtpResponse(BaseModel):
    method: CtpMethod
    
    RspInfo: RspInfoField = RspInfoField()
    RequestID: Optional[int] = None
    IsLast: bool = True
    
    @property
    def args(self) -> list[any]:
        return []


class RspUserLogin(CtpResponse):
    method: CtpMethod = CtpMethod.OnRspUserLogin

    RspUserLogin: Optional[RspUserLoginField]
    
    @property
    def args(self) -> list[any]:
        return [self.RspUserLogin, self.RspInfo, self.RequestID, self.IsLast]


class RspSubMarketData(CtpResponse):
    method: CtpMethod = CtpMethod.OnRspSubMarketData
    
    SpecificInstrument: Optional[SpecificInstrumentField]
    
    @property
    def args(self) -> list[any]:
        return [self.SpecificInstrument, self.RspInfo, self.RequestID, self.IsLast]


class RtnDepthMarketData(CtpResponse):
    method: CtpMethod = CtpMethod.OnRtnDepthMarketData
    
    DepthMarketData: Optional[DepthMarketDataField]
    
    @property
    def args(self) -> list[any]:
        return [self.DepthMarketData]
