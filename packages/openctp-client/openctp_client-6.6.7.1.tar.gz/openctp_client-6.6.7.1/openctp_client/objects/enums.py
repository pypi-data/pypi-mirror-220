from enum import Enum, auto


class CtpMethod(Enum):
    Connect = auto()
    Disconnect = auto()
    SubscribeMarketData = auto()
    OnRspUserLogin = auto()
    OnRspSubMarketData = auto()
    OnRtnDepthMarketData = auto()

    ReqSettlementInfoConfirm = auto()
    OnRspSettlementInfoConfirm = auto()
    ReqOrderInsert = auto()
    OnOrderInsert = auto()
    OnErrRtnOrderInsert = auto()
    OnRtnTrade = auto()
    
    @classmethod
    def nameOf(cls, name):
        return cls.__members__.get(name, None)
