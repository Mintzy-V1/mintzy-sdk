from typing import Dict, Any, Optional
from mintzy.models.session import (
    AuthenticateResponse, VerifyTotpResponse, 
    StartTradingResponse, StopTradingResponse, DashboardResponse
)

class SessionsClient:
    """Client for managing Mintzy trading sessions."""
    
    def __init__(self, request_func):
        self._request = request_func

    def authenticate(self, api_key: str, client_code: str, password: str) -> AuthenticateResponse:
        """Authenticate with the trading plugin."""
        payload = {
            "broker_type": "angel",
            "api_key": api_key,
            "client_code": client_code,
            "password": password
        }
        response = self._request("POST", "/api/plugin/credentials", json=payload)
        return AuthenticateResponse(**response.json())

    def verify_totp(self, session_id: str, totp: str) -> VerifyTotpResponse:
        """Verify TOTP for trading session."""
        payload = {
            "session_id": session_id,
            "totp": totp
        }
        response = self._request("POST", "/api/plugin/totp", json=payload)
        return VerifyTotpResponse(**response.json())

    def start(self, session_id: str, saved_configuration_id: Optional[str] = None, **kwargs) -> StartTradingResponse:
        """Start trading session."""
        payload = {"session_id": session_id}
        if saved_configuration_id:
            payload["saved_configuration_id"] = saved_configuration_id
        payload.update(kwargs)
        response = self._request("POST", "/api/plugin/start", json=payload)
        return StartTradingResponse(**response.json())

    def stop(self, session_id: str) -> StopTradingResponse:
        """Stop trading session."""
        payload = {"session_id": session_id}
        response = self._request("POST", "/api/plugin/stop", json=payload)
        return StopTradingResponse(**response.json())

    def exit_position(self, session_id: str, symbol: str) -> Dict[str, Any]:
        """Exit a specific position."""
        response = self._request("POST", f"/api/plugin/exit-symbol/{session_id}/{symbol}")
        return response.json()

    def get_dashboard(self, session_id: Optional[str] = None) -> DashboardResponse:
        """Get the trading dashboard state."""
        params = {}
        if session_id:
            params["session_id"] = session_id
        response = self._request("GET", "/api/plugin/dashboard", params=params)
        return DashboardResponse(**response.json())

    def get_session(self) -> Dict[str, Any]:
        """Get session state or restore via token."""
        response = self._request("GET", "/api/plugin/session")
        return response.json()

    def get_trades(self, session_id: str) -> Dict[str, Any]:
        """Trading logs for session."""
        response = self._request("GET", f"/api/plugin/sessions/{session_id}/trades")
        return response.json()

    def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Session status from plugin DB."""
        response = self._request("GET", f"/api/plugin/sessions/{session_id}/status")
        return response.json()

    def list_sessions(self) -> Dict[str, Any]:
        """List all user sessions."""
        response = self._request("GET", "/api/plugin/tradingsessions")
        return response.json()

    def get_active_session(self) -> Dict[str, Any]:
        """Current active session."""
        response = self._request("GET", "/api/plugin/trading/active-session")
        return response.json()

    def get_session_by_id(self, session_id: str) -> Dict[str, Any]:
        """Get session metadata."""
        response = self._request("GET", f"/api/plugin/trading/sessions/{session_id}")
        return response.json()

    def abandon(self, session_id: str) -> Dict[str, Any]:
        """Abandon session."""
        response = self._request("POST", f"/api/plugin/trading/{session_id}/abandon")
        return response.json()

    def download_tradebook(self, session_id: str) -> str:
        """Download CSV tradebook."""
        response = self._request("GET", f"/api/plugin/trading/{session_id}/final-tradebook")
        return response.text

    def download_logs(self, session_id: str) -> str:
        """Download logs as CSV."""
        response = self._request("GET", f"/api/plugin/sessions/{session_id}/download")
        return response.text
