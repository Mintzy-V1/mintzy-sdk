from typing import Dict, Any

class AdminClient:
    """Client for Mintzy admin operations."""
    def __init__(self, request_func):
        self._request = request_func

    def stop_session(self, session_id: str) -> Dict[str, Any]:
        """Admin force stop a session."""
        response = self._request("POST", f"/api/plugin/admin/sessions/{session_id}/stop")
        return response.json()

    def force_stop_all(self) -> Dict[str, Any]:
        """Admin force stop all sessions."""
        response = self._request("POST", "/api/plugin/admin/force-stop-all")
        return response.json()
