from typing import ClassVar, Optional
from pydantic import BaseModel, Field, constr
from openctp_ctp import tdapi


class CtpField(BaseModel):
    _ctp_type_: ClassVar[callable] = None

    def ctp_object(self) -> any:
        obj = self._ctp_type_()
        for key, value in self.dict().items():
            if value is not None:
                setattr(obj, key, value)
        return obj

    class Config:
        orm_mode = True


class ReqUserLoginField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcReqUserLoginField
    
    TradingDay: Optional[constr(max_length=9)] = Field(None, description='交易日')
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    UserID: Optional[constr(max_length=16)] = Field(None, description='用户代码')
    Password: Optional[constr(max_length=41)] = Field(None, description='密码')
    UserProductInfo: Optional[constr(max_length=11)] = Field(
        None, description='用户端产品信息'
    )
    InterfaceProductInfo: Optional[constr(max_length=11)] = Field(
        None, description='接口端产品信息'
    )
    ProtocolInfo: Optional[constr(max_length=11)] = Field(None, description='协议信息')
    MacAddress: Optional[constr(max_length=21)] = Field(None, description='Mac地址')
    OneTimePassword: Optional[constr(max_length=41)] = Field(None, description='动态密码')
    reserve1: Optional[constr(max_length=16)] = Field(None, description='保留的无效字段')
    LoginRemark: Optional[constr(max_length=36)] = Field(None, description='登录备注')
    ClientIPPort: Optional[int] = Field(None, description='终端IP端口')
    ClientIPAddress: Optional[constr(max_length=33)] = Field(None, description='终端IP地址')


class RspUserLoginField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcRspUserLoginField
    
    TradingDay: Optional[constr(max_length=9)] = Field(None, description='交易日')
    LoginTime: Optional[constr(max_length=9)] = Field(None, description='登录成功时间')
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    UserID: Optional[constr(max_length=16)] = Field(None, description='用户代码')
    SystemName: Optional[constr(max_length=41)] = Field(None, description='交易系统名称')
    FrontID: Optional[int] = Field(None, description='前置编号')
    SessionID: Optional[int] = Field(None, description='会话编号')
    MaxOrderRef: Optional[constr(max_length=13)] = Field(None, description='最大报单引用')
    SHFETime: Optional[constr(max_length=9)] = Field(None, description='上期所时间')
    DCETime: Optional[constr(max_length=9)] = Field(None, description='大商所时间')
    CZCETime: Optional[constr(max_length=9)] = Field(None, description='郑商所时间')
    FFEXTime: Optional[constr(max_length=9)] = Field(None, description='中金所时间')
    INETime: Optional[constr(max_length=9)] = Field(None, description='能源中心时间')
    SysVersion: Optional[constr(max_length=41)] = Field(None, description='后台版本信息')


class UserLogoutField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcUserLogoutField
    
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    UserID: Optional[constr(max_length=16)] = Field(None, description='用户代码')


class ReqAuthenticateField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcReqAuthenticateField
    
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    UserID: Optional[constr(max_length=16)] = Field(None, description='用户代码')
    UserProductInfo: Optional[constr(max_length=11)] = Field(
        None, description='用户端产品信息'
    )
    AuthCode: Optional[constr(max_length=17)] = Field(None, description='认证码')
    AppID: Optional[constr(max_length=33)] = Field(None, description='App代码')


class RspAuthenticateField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcRspAuthenticateField
    
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    UserID: Optional[constr(max_length=16)] = Field(None, description='用户代码')
    UserProductInfo: Optional[constr(max_length=11)] = Field(
        None, description='用户端产品信息'
    )
    AppID: Optional[constr(max_length=33)] = Field(None, description='App代码')
    AppType: Optional[constr(max_length=1)] = Field(None, description='App类型')


class AuthenticationInfoField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcAuthenticationInfoField
    
    BrokerID: Optional[constr(max_length=11)] = Field(None, description='经纪公司代码')
    UserID: Optional[constr(max_length=16)] = Field(None, description='用户代码')
    UserProductInfo: Optional[constr(max_length=11)] = Field(
        None, description='用户端产品信息'
    )
    AuthInfo: Optional[constr(max_length=129)] = Field(None, description='认证信息')
    IsResult: Optional[int] = Field(None, description='是否为认证结果')
    AppID: Optional[constr(max_length=33)] = Field(None, description='App代码')
    AppType: Optional[constr(max_length=1)] = Field(None, description='App类型')
    reserve1: Optional[constr(max_length=16)] = Field(None, description='保留的无效字段')
    ClientIPAddress: Optional[constr(max_length=33)] = Field(None, description='终端IP地址')


class RspInfoField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcRspInfoField
    
    ErrorID: Optional[int] = Field(None, description='错误代码')
    ErrorMsg: Optional[constr(max_length=81)] = Field(None, description='错误信息')
    
class ExchangeField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcExchangeField
    
    ExchangeID: Optional[constr(max_length=9)] = Field(None, description='交易所代码')
    ExchangeName: Optional[constr(max_length=61)] = Field(None, description='交易所名称')
    ExchangeProperty: Optional[constr(max_length=1)] = Field(None, description='交易所属性')


class ProductField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcProductField
    
    reserve1: Optional[constr(max_length=31)] = Field(None, description='保留的无效字段')
    ProductName: Optional[constr(max_length=21)] = Field(None, description='产品名称')
    ExchangeID: Optional[constr(max_length=9)] = Field(None, description='交易所代码')
    ProductClass: Optional[constr(max_length=1)] = Field(None, description='产品类型')
    VolumeMultiple: Optional[int] = Field(None, description='合约数量乘数')
    PriceTick: Optional[float] = Field(None, description='最小变动价位')
    MaxMarketOrderVolume: Optional[int] = Field(None, description='市价单最大下单量')
    MinMarketOrderVolume: Optional[int] = Field(None, description='市价单最小下单量')
    MaxLimitOrderVolume: Optional[int] = Field(None, description='限价单最大下单量')
    MinLimitOrderVolume: Optional[int] = Field(None, description='限价单最小下单量')
    PositionType: Optional[constr(max_length=1)] = Field(None, description='持仓类型')
    PositionDateType: Optional[constr(max_length=1)] = Field(None, description='持仓日期类型')
    CloseDealType: Optional[constr(max_length=1)] = Field(None, description='平仓处理类型')
    TradeCurrencyID: Optional[constr(max_length=4)] = Field(None, description='交易币种类型')
    MortgageFundUseRange: Optional[constr(max_length=1)] = Field(
        None, description='质押资金可用范围'
    )
    reserve2: Optional[constr(max_length=31)] = Field(None, description='保留的无效字段')
    UnderlyingMultiple: Optional[float] = Field(None, description='合约基础商品乘数')
    ProductID: Optional[constr(max_length=81)] = Field(None, description='产品代码')
    ExchangeProductID: Optional[constr(max_length=81)] = Field(
        None, description='交易所产品代码'
    )
    OpenLimitControlLevel: Optional[constr(max_length=1)] = Field(
        None, description='开仓量限制粒度'
    )
    OrderFreqControlLevel: Optional[constr(max_length=1)] = Field(
        None, description='报单频率控制粒度'
    )


class InstrumentField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcInstrumentField
    
    reserve1: Optional[constr(max_length=31)] = Field(None, description='保留的无效字段')
    ExchangeID: Optional[constr(max_length=9)] = Field(None, description='交易所代码')
    InstrumentName: Optional[constr(max_length=21)] = Field(None, description='合约名称')
    reserve2: Optional[constr(max_length=31)] = Field(None, description='保留的无效字段')
    reserve3: Optional[constr(max_length=31)] = Field(None, description='保留的无效字段')
    ProductClass: Optional[constr(max_length=1)] = Field(None, description='产品类型')
    DeliveryYear: Optional[int] = Field(None, description='交割年份')
    DeliveryMonth: Optional[int] = Field(None, description='交割月')
    MaxMarketOrderVolume: Optional[int] = Field(None, description='市价单最大下单量')
    MinMarketOrderVolume: Optional[int] = Field(None, description='市价单最小下单量')
    MaxLimitOrderVolume: Optional[int] = Field(None, description='限价单最大下单量')
    MinLimitOrderVolume: Optional[int] = Field(None, description='限价单最小下单量')
    VolumeMultiple: Optional[int] = Field(None, description='合约数量乘数')
    PriceTick: Optional[float] = Field(None, description='最小变动价位')
    CreateDate: Optional[constr(max_length=9)] = Field(None, description='创建日')
    OpenDate: Optional[constr(max_length=9)] = Field(None, description='上市日')
    ExpireDate: Optional[constr(max_length=9)] = Field(None, description='到期日')
    StartDelivDate: Optional[constr(max_length=9)] = Field(None, description='开始交割日')
    EndDelivDate: Optional[constr(max_length=9)] = Field(None, description='结束交割日')
    InstLifePhase: Optional[constr(max_length=1)] = Field(None, description='合约生命周期状态')
    IsTrading: Optional[int] = Field(None, description='当前是否交易')
    PositionType: Optional[constr(max_length=1)] = Field(None, description='持仓类型')
    PositionDateType: Optional[constr(max_length=1)] = Field(None, description='持仓日期类型')
    LongMarginRatio: Optional[float] = Field(None, description='多头保证金率')
    ShortMarginRatio: Optional[float] = Field(None, description='空头保证金率')
    MaxMarginSideAlgorithm: Optional[constr(max_length=1)] = Field(
        None, description='是否使用大额单边保证金算法'
    )
    reserve4: Optional[constr(max_length=31)] = Field(None, description='保留的无效字段')
    StrikePrice: Optional[float] = Field(None, description='执行价')
    OptionsType: Optional[constr(max_length=1)] = Field(None, description='期权类型')
    UnderlyingMultiple: Optional[float] = Field(None, description='合约基础商品乘数')
    CombinationType: Optional[constr(max_length=1)] = Field(None, description='组合类型')
    InstrumentID: Optional[constr(max_length=81)] = Field(None, description='合约代码')
    ExchangeInstID: Optional[constr(max_length=81)] = Field(
        None, description='合约在交易所的代码'
    )
    ProductID: Optional[constr(max_length=81)] = Field(None, description='产品代码')
    UnderlyingInstrID: Optional[constr(max_length=81)] = Field(
        None, description='基础商品代码'
    )


class SpecificInstrumentField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcSpecificInstrumentField
    
    reserve1: Optional[constr(max_length=31)] = Field(None, description='保留的无效字段')
    InstrumentID: Optional[constr(max_length=81)] = Field(None, description='合约代码')
    
    
class DepthMarketDataField(CtpField):
    _ctp_type_ = tdapi.CThostFtdcDepthMarketDataField
    
    TradingDay: Optional[constr(max_length=9)] = Field(None, description='交易日')
    reserve1: Optional[constr(max_length=31)] = Field(None, description='保留的无效字段')
    ExchangeID: Optional[constr(max_length=9)] = Field(None, description='交易所代码')
    reserve2: Optional[constr(max_length=31)] = Field(None, description='保留的无效字段')
    LastPrice: Optional[float] = Field(None, description='最新价')
    PreSettlementPrice: Optional[float] = Field(None, description='上次结算价')
    PreClosePrice: Optional[float] = Field(None, description='昨收盘')
    PreOpenInterest: Optional[float] = Field(None, description='昨持仓量')
    OpenPrice: Optional[float] = Field(None, description='今开盘')
    HighestPrice: Optional[float] = Field(None, description='最高价')
    LowestPrice: Optional[float] = Field(None, description='最低价')
    Volume: Optional[int] = Field(None, description='数量')
    Turnover: Optional[float] = Field(None, description='成交金额')
    OpenInterest: Optional[float] = Field(None, description='持仓量')
    ClosePrice: Optional[float] = Field(None, description='今收盘')
    SettlementPrice: Optional[float] = Field(None, description='本次结算价')
    UpperLimitPrice: Optional[float] = Field(None, description='涨停板价')
    LowerLimitPrice: Optional[float] = Field(None, description='跌停板价')
    PreDelta: Optional[float] = Field(None, description='昨虚实度')
    CurrDelta: Optional[float] = Field(None, description='今虚实度')
    UpdateTime: Optional[constr(max_length=9)] = Field(None, description='最后修改时间')
    UpdateMillisec: Optional[int] = Field(None, description='最后修改毫秒')
    BidPrice1: Optional[float] = Field(None, description='申买价一')
    BidVolume1: Optional[int] = Field(None, description='申买量一')
    AskPrice1: Optional[float] = Field(None, description='申卖价一')
    AskVolume1: Optional[int] = Field(None, description='申卖量一')
    BidPrice2: Optional[float] = Field(None, description='申买价二')
    BidVolume2: Optional[int] = Field(None, description='申买量二')
    AskPrice2: Optional[float] = Field(None, description='申卖价二')
    AskVolume2: Optional[int] = Field(None, description='申卖量二')
    BidPrice3: Optional[float] = Field(None, description='申买价三')
    BidVolume3: Optional[int] = Field(None, description='申买量三')
    AskPrice3: Optional[float] = Field(None, description='申卖价三')
    AskVolume3: Optional[int] = Field(None, description='申卖量三')
    BidPrice4: Optional[float] = Field(None, description='申买价四')
    BidVolume4: Optional[int] = Field(None, description='申买量四')
    AskPrice4: Optional[float] = Field(None, description='申卖价四')
    AskVolume4: Optional[int] = Field(None, description='申卖量四')
    BidPrice5: Optional[float] = Field(None, description='申买价五')
    BidVolume5: Optional[int] = Field(None, description='申买量五')
    AskPrice5: Optional[float] = Field(None, description='申卖价五')
    AskVolume5: Optional[int] = Field(None, description='申卖量五')
    AveragePrice: Optional[float] = Field(None, description='当日均价')
    ActionDay: Optional[constr(max_length=9)] = Field(None, description='业务日期')
    InstrumentID: Optional[constr(max_length=81)] = Field(None, description='合约代码')
    ExchangeInstID: Optional[constr(max_length=81)] = Field(
        None, description='合约在交易所的代码'
    )
    BandingUpperPrice: Optional[float] = Field(None, description='上带价')
    BandingLowerPrice: Optional[float] = Field(None, description='下带价')
