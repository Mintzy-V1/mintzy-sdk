# This script demonstrates how an end user would use the Mintzy SDK
# to authenticate their broker using the new Plugin API Key.

import sys
import os

# (This sys.path manipulation is just so we use the local SDK code without pip installing it)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from mintzy import MintzyClient
from mintzy.exceptions import MintzyAuthError, MintzyAPIError

def main():
    # 1. Initialize the MintzyClient with the Plugin API Key
    # (End users will not need the base_url parameter once deployed to production)
    api_key = "sk_trade_dbace7199359a6398b3b48d8dd8af961f42c447ad315c9b14ca3f778f53a11b3"
    client = MintzyClient(api_key=api_key, base_url="http://localhost:5000")
    
    print("Mintzy Client Initialized.")
    print("Attempting to authenticate broker credentials with the backend...")

    try:
        # 2. Authenticate with the broker
        auth_resp = client.trading.sessions.authenticate(
            api_key="dummy_broker_api_key",
            client_code="dummy_client_code",
            password="dummy_password"
        )
        
        session_id = auth_resp.session_id
        print(f"Successfully authenticated! Session ID: {session_id}")
        
        # 3. Verify TOTP (commented out as it requires a real session)
        # print("Verifying TOTP...")
        # client.trading.sessions.verify_totp(session_id=session_id, totp="123456")
        # print("TOTP Verified!")
        
    except MintzyAuthError as e:
        print(f"\n[Auth Error] Failed to authenticate: {e}")
    except MintzyAPIError as e:
        print(f"\n[API Error] An error occurred: {e}")
    except Exception as e:
        print(f"\n[Error] Unexpected error: {e}")

if __name__ == "__main__":
    main()
