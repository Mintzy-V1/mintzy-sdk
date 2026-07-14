import time
import certifi
import httpx
from typing import Any

from mintzy.exceptions import (
    MintzyAuthError, MintzyValidationError, MintzyRateLimitError,
    MintzyServerError, MintzyConnectionError, MintzyTimeoutError, MintzyAPIError
)
from mintzy.trading.client import TradingClient
from mintzy.trading.admin import AdminClient

class MintzyClient:
    """The root Mintzy API client."""
    
    def __init__(self, api_key: str, base_url: str = "https://api.mintzy.in", verify_ssl: bool = True):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        
        self._client = httpx.Client(
            base_url=self.base_url,
            verify=verify_ssl,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            }
        )
        
        # Sub-clients
        self.trading = TradingClient(self._request)
        self.admin = AdminClient(self._request)

    def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        retries = 3
        delays = [0.5, 1.0, 2.0]
        
        for attempt in range(retries + 1):
            try:
                response = self._client.request(method, url, **kwargs)
                if response.status_code in (502, 503, 504) and attempt < retries:
                    time.sleep(delays[attempt])
                    continue
                
                self._raise_for_status(response)
                return response
                
            except httpx.TimeoutException as e:
                if attempt < retries:
                    time.sleep(delays[attempt])
                    continue
                raise MintzyTimeoutError(f"Request timed out: {str(e)}") from e
            except httpx.RequestError as e:
                if attempt < retries:
                    time.sleep(delays[attempt])
                    continue
                raise MintzyConnectionError(f"Request failed: {str(e)}") from e
                
        raise MintzyServerError("Max retries exceeded", 500)

    def _raise_for_status(self, response: httpx.Response) -> None:
        if 400 <= response.status_code < 600:
            status = response.status_code
            try:
                body = response.json()
            except Exception:
                body = response.text
                
            msg = f"API request failed with status {status}: {body}"
            
            if status in (401, 403):
                raise MintzyAuthError(msg, status, response.text)
            elif status in (400, 422):
                raise MintzyValidationError(msg, status, response.text)
            elif status == 429:
                raise MintzyRateLimitError(msg, status, response.text)
            elif status >= 500:
                raise MintzyServerError(msg, status, response.text)
            else:
                raise MintzyAPIError(msg, status, response.text)
                
    def close(self):
        self._client.close()

    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
