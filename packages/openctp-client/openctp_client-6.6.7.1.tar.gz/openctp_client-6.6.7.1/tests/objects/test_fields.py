from openctp_ctp import tdapi
from openctp_client.objects import *


def test_should_return_CThostFtdcReqUserLoginField_when_ctp_object():
    login_field = ReqUserLoginField(
        TradingDay="20190101",
        BrokerID="99999",
    )
    
    ctp_login = login_field.ctp_object()
    assert isinstance(ctp_login, tdapi.CThostFtdcReqUserLoginField) is True
    assert ctp_login.TradingDay == login_field.TradingDay
    assert ctp_login.BrokerID == login_field.BrokerID


def test_should_return_RspUserLoginField_when_from_ctp_object():
    ctp_login: tdapi.CThostFtdcRspUserLoginField = tdapi.CThostFtdcRspUserLoginField()
    ctp_login.TradingDay = "20190101"
    ctp_login.BrokerID = "99999"
    
    login_field = ReqUserLoginField.from_ctp_object(ctp_login)
    assert isinstance(login_field, ReqUserLoginField) is True
    assert login_field.TradingDay == ctp_login.TradingDay
    assert login_field.BrokerID == ctp_login.BrokerID


def test_should_return_None_when_from_ctp_object_given_None():
    login_field = ReqUserLoginField.from_ctp_object(None)
    assert login_field is None
