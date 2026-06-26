from mintzy.trading.sessions import SessionsClient
from mintzy.trading.pnl import PnLClient
from mintzy.trading.configurations import ConfigurationsClient

class TradingClient:
    """Client for the Mintzy Trading API."""
    
    def __init__(self, request_func):
        self.sessions = SessionsClient(request_func)
        self.pnl = PnLClient(request_func)
        self.configurations = ConfigurationsClient(request_func)
