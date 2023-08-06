import pytest
from pytest_mock import mocker, MockerFixture

from openctp_client.clients.simple_ctp_client import MdClient
from openctp_client.objects import *


@pytest.fixture
def spi_callback():
    def callback(*args, **kwargs):
        pass
    return callback

@pytest.fixture
def config():
    conf = CtpConfig("tcp://test_address", "borker_id", "auth_code", "appi_id", "", "")
    return conf


def test_should_get_spi_callback_when_add_spi_callback_to_md_client(config: CtpConfig, spi_callback):
    client = MdClient(config)
    client.add_spi_callback(CtpMethod.OnOrderInsert, spi_callback)
    callbacks = client.get_spi_callback(CtpMethod.OnOrderInsert)
    assert len(callbacks) == 1
    assert callbacks[0] == spi_callback

def test_should_get_none_when_del_spi_callback_from_md_client(config: CtpConfig, spi_callback):
    client = MdClient(config)
    client.add_spi_callback(CtpMethod.OnOrderInsert, spi_callback)
    client.del_spi_callback(CtpMethod.OnOrderInsert, spi_callback)
    callbacks = client.get_spi_callback(CtpMethod.OnOrderInsert)
    assert len(callbacks) == 0

def test_should_call_Init_when_Connect(config: CtpConfig, mocker: MockerFixture):
    mdapi = mocker.patch("openctp_client.clients.simple_ctp_client.mdapi")
    api = mocker.Mock(name="api")
    mdapi.CThostFtdcMdApi.CreateFtdcMdApi.return_value = api
    
    client = MdClient(config)
    client.Connect()
    
    assert api.Init.called_once
    