from typing import Optional, Dict, Any
from mintzy.models.config import ConfigurationResponse

class ConfigurationsClient:
    """Client for managing Mintzy trading configurations."""
    
    def __init__(self, request_func):
        self._request = request_func

    def create(self, name: str, configuration: Dict[str, Any], description: Optional[str] = None) -> ConfigurationResponse:
        """Create a new saved configuration."""
        payload = {"name": name, "configuration": configuration}
        if description: payload["description"] = description
        response = self._request("POST", "/api/plugin/saved-configurations", json=payload)
        return ConfigurationResponse(**response.json())

    def get(self, config_id: str) -> ConfigurationResponse:
        """Get a saved configuration by ID."""
        response = self._request("GET", f"/api/plugin/saved-configurations/{config_id}")
        return ConfigurationResponse(**response.json())

    def update(self, config_id: str, name: Optional[str] = None, configuration: Optional[Dict[str, Any]] = None, description: Optional[str] = None) -> ConfigurationResponse:
        """Update an existing configuration."""
        payload = {}
        if name is not None: payload["name"] = name
        if configuration is not None: payload["configuration"] = configuration
        if description is not None: payload["description"] = description
        response = self._request("PUT", f"/api/plugin/saved-configurations/{config_id}", json=payload)
        return ConfigurationResponse(**response.json())

    def delete(self, config_id: str) -> Dict[str, Any]:
        """Delete a saved configuration."""
        response = self._request("DELETE", f"/api/plugin/saved-configurations/{config_id}")
        return response.json()
