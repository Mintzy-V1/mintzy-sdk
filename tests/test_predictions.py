import pytest
import respx
import httpx
from mintzy.exceptions import MintzyValidationError

@respx.mock
def test_get_prediction_success(client):
    respx.post("https://api.mintzy.com/api/stock/prediction").mock(return_value=httpx.Response(200, json={
        "result": {
            "TCS": {
                "close": {
                    "predicted_prices": [3500.0, 3505.0],
                    "timestamps": ["2023-10-01T10:00:00", "2023-10-01T10:01:00"]
                }
            }
        }
    }))
    respx.get("https://api.mintzy.com/api/user/credits").mock(return_value=httpx.Response(200, json={"credits": 95}))
    
    response = client.predictions.get_prediction("TCS", "20 minutes", "close", "1m")
    assert response.success is True
    assert len(response.data) == 2
    assert response.data[0].Ticker == "TCS"
    assert response.data[0].Predicted_Price == 3500.0
    assert response.credits_remaining == 95

def test_get_prediction_invalid_ticker(client):
    with pytest.raises(MintzyValidationError, match="Ticker\\(s\\) not supported currently"):
        client.predictions.get_prediction("INVALID", "20 minutes", "close")
