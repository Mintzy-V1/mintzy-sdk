from typing import Optional, Dict, Any, Generator
import time
from mintzy.models.pnl import AggregatePnL, LivePnL

class PnLClient:
    """Client for accessing Mintzy PnL data."""
    
    def __init__(self, request_func):
        self._request = request_func

    def get_pnl(self, session_id: Optional[str] = None, year: Optional[int] = None, month: Optional[int] = None) -> AggregatePnL:
        """Get general PnL data."""
        params = {}
        if session_id: params["session_id"] = session_id
        if year: params["year"] = year
        if month: params["month"] = month
        response = self._request("GET", "/api/plugin/dashboard/pnl", params=params)
        return AggregatePnL(**response.json())

    def get_aggregate_pnl(self, year: Optional[int] = None, month: Optional[int] = None) -> AggregatePnL:
        """Get aggregate PnL data for the user."""
        params = {}
        if year: params["year"] = year
        if month: params["month"] = month
        response = self._request("GET", "/api/plugin/dashboard/pnl/aggregate", params=params)
        return AggregatePnL(**response.json())

    def get_live_pnl(self, session_id: str) -> LivePnL:
        """Get the live PnL for a specific session."""
        response = self._request("GET", f"/api/plugin/trading/live-pnl/{session_id}")
        return LivePnL(**response.json())

    def get_pnl_history(self, session_id: str, date: Optional[str] = None) -> Dict[str, Any]:
        """Get the PnL history for a session."""
        params = {}
        if date: params["date"] = date
        response = self._request("GET", f"/api/plugin/trading/live-pnl/{session_id}/history", params=params)
        return response.json()

    def stream_pnl(self, session_id: str) -> Generator[LivePnL, None, None]:
        """Poll the live PnL endpoint every 30 seconds and yield snapshots."""
        while True:
            yield self.get_live_pnl(session_id)
            time.sleep(30)
