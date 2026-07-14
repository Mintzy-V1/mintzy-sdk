import sys, os
sys.path.insert(0, os.path.abspath('src'))
from mintzy import MintzyClient
try:
    client = MintzyClient(api_key="sk_trade_bfe3a542baa51d7ed3eebd9f93bab2052137b96e93496329b1f9e19d8b00e114", base_url="http://localhost:5000")
    print("Sending auth request...")
    resp = client.trading.sessions.authenticate("GKZMppc5", "AACA090802", "2004")
    print(resp)
except Exception as e:
    print(f"Exception Type: {type(e)}")
    print(f"Exception String: {str(e)}")
    if hasattr(e, 'status_code'):
        print(f"Status Code: {e.status_code}")
    if hasattr(e, 'response_body'):
        print(f"Response Body: {e.response_body}")
