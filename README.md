# Mintzy Python SDK

The official Python SDK for Mintzy.

## Installation

```bash
pip install mintzy
```

## Quickstart: Trading Flow

```python
from mintzy import MintzyClient

client = MintzyClient(api_key="sk_live_...")

# 1. Authenticate
auth_resp = client.trading.sessions.authenticate(
    api_key="broker_api_key",
    client_code="client_code",
    password="password"
)
session_id = auth_resp.session_id

# 2. Verify TOTP
client.trading.sessions.verify_totp(session_id=session_id, totp="123456")

# 3. Start Trading
client.trading.sessions.start(session_id=session_id)

# 4. Stop Trading
client.trading.sessions.stop(session_id=session_id)
```

## API Reference

### Trading Sessions (`client.trading.sessions`)
| Method | Description |
|--------|-------------|
| `authenticate(...)` | Authenticate with the broker. |
| `verify_totp(...)` | Verify 2FA TOTP. |
| `start(...)` | Start a trading session. |
| `stop(...)` | Stop a trading session. |
| `exit_position(...)` | Exit a specific position. |
| `get_dashboard(...)` | Get the trading dashboard state. |

### Trading PnL (`client.trading.pnl`)
| Method | Description |
|--------|-------------|
| `get_pnl(...)` | Get general PnL data. |
| `get_aggregate_pnl(...)` | Get aggregate PnL data. |
| `get_live_pnl(...)` | Get live PnL for a session. |
| `get_pnl_history(...)` | Get PnL history for a session. |
| `stream_pnl(...)` | Generator to stream live PnL every 30s. |

### Trading Configurations (`client.trading.configurations`)
| Method | Description |
|--------|-------------|
| `create(...)` | Create a configuration. |
| `get(...)` | Get a configuration by ID. |
| `update(...)` | Update a configuration. |
| `delete(...)` | Delete a configuration. |
