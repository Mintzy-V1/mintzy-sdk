import os
import sys

# Ensure we use the local mintzy SDK
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from mintzy import MintzyClient
from mintzy.exceptions import MintzyAuthError, MintzyAPIError

def test_key():
    api_key = "sk_trade_dbace7199359a6398b3b48d8dd8af961f42c447ad315c9b14ca3f778f53a11b3"
    base_url = "http://localhost:5000"
    
    print(f"Testing Plugin API Key: {api_key}")
    print(f"Connecting to: {base_url}")
    
    try:
        with MintzyClient(api_key=api_key, base_url=base_url) as client:
            print("\nAttempting to call client.trading.sessions.list_sessions()...")
            sessions = client.trading.sessions.list_sessions()
            print("Success! Response:")
            print(sessions)
            
    except MintzyAuthError as e:
        print(f"\nAuthentication Error! The key was rejected.")
        print(f"Status: {e.status_code}")
        print(f"Message: {e}")
    except MintzyAPIError as e:
        print(f"\nAPI Error: {e.status_code}")
        print(f"Message: {e}")
    except Exception as e:
        print(f"\nUnexpected error: {e}")

if __name__ == "__main__":
    test_key()
