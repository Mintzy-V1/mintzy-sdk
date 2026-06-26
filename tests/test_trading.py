import pytest
import respx
import httpx
from mintzy.exceptions import MintzyAuthError

@respx.mock
def test_authenticate(client):
    respx.post("https://api.mintzy.com/api/plugin/authenticate").mock(
        return_value=httpx.Response(200, json={"session_id": "sess_123", "message": "Success"})
    )
    
    response = client.trading.sessions.authenticate("api_key", "client_code", "password")
    assert response.session_id == "sess_123"

@respx.mock
def test_get_pnl(client):
    respx.get("https://api.mintzy.com/api/plugin/pnl?session_id=sess_123").mock(
        return_value=httpx.Response(200, json={
            "total_pnl": 150.5,
            "records": [{"date": "2023-10-01", "pnl": 150.5}]
        })
    )
    
    response = client.trading.pnl.get_pnl(session_id="sess_123")
    assert response.total_pnl == 150.5
    assert len(response.records) == 1

@respx.mock
def test_auth_error(client):
    respx.post("https://api.mintzy.com/api/plugin/authenticate").mock(
        return_value=httpx.Response(401, json={"error": "Unauthorized"})
    )
    
    with pytest.raises(MintzyAuthError):
        client.trading.sessions.authenticate("wrong", "wrong", "wrong")
