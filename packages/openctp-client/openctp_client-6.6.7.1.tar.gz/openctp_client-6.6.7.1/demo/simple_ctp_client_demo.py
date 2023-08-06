from openctp_client.objects import *
from openctp_client.objects.enums import CtpMethod
from openctp_client.clients.simple_ctp_client import MdClient

if __name__ == "__main__":
    config = CtpConfig("tcp://180.168.146.187:10211", "9999", "9999", "9999", "9999", "9999")
    client = MdClient(config)
    
    def connected(login_info: RspUserLoginField, rsp_info: RspInfoField, request_id: int, last: bool):
        print(f"connected: {login_info.TradingDay}")
        client.SubscribeMarketData(["ag2308"])
    
    def on_subscribe_market_data(instrument: SpecificInstrumentField, rsp_info: RspInfoField, request_id: int, last: bool):
        print(f"subscribe market data: {instrument.InstrumentID}")
    
    def on_market_data(data: DepthMarketDataField):
        print(f"market data: {data.InstrumentID} {data.AskPrice1}")
    
    client.add_spi_callback(CtpMethod.OnRspUserLogin, connected)
    client.add_spi_callback(CtpMethod.OnRspSubMarketData, on_subscribe_market_data)
    client.add_spi_callback(CtpMethod.OnRtnDepthMarketData, on_market_data)
    
    client.Connect()
    
    ch = input("press any key to exit")
