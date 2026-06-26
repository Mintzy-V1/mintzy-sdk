"""Exceptions for the Mintzy SDK."""

class MintzyError(Exception):
    """Base exception for all Mintzy SDK errors."""
    pass

class MintzyAPIError(MintzyError):
    """Exception raised for API errors (HTTP 4xx/5xx)."""
    def __init__(self, message: str, status_code: int, response_body: str = ""):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body

class MintzyAuthError(MintzyAPIError):
    """Exception raised for authentication errors (HTTP 401/403)."""
    pass

class MintzyValidationError(MintzyAPIError):
    """Exception raised for validation errors (HTTP 422/400)."""
    pass

class MintzyRateLimitError(MintzyAPIError):
    """Exception raised for rate limiting (HTTP 429)."""
    pass

class MintzyServerError(MintzyAPIError):
    """Exception raised for server errors (HTTP 5xx)."""
    pass

class MintzyConnectionError(MintzyError):
    """Exception raised when connection to the API fails."""
    pass

class MintzyTimeoutError(MintzyConnectionError):
    """Exception raised when an API request times out."""
    pass
