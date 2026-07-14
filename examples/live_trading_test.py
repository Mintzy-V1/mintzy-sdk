import sys
import os
import time

# Ensure we use the local SDK from src/ instead of any pip installed version
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from mintzy import MintzyClient
from mintzy.exceptions import MintzyError, MintzyAuthError

def main():
    print("=" * 60)
    print(" Mintzy Live Trading End-User Test")
    print("=" * 60)

    # Ask the user for their live API token
    api_key = input("Enter your Mintzy API Key (sk_live_...): ").strip()
    
    # Initialize the client. By default, it hits https://api.mintzy.in
    # For local dev testing, you can pass base_url="http://localhost:5000"
    try:
        client = MintzyClient(api_key=api_key, verify_ssl=False)
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return

    print("\n1. Broker Authentication")
    broker_api_key = input("  Upstox API Key: ").strip()
    client_code = input("  Upstox Client Code: ").strip()
    password = input("  Upstox Password: ").strip()

    print("\n🔄 Authenticating with backend...")
    try:
        auth_resp = client.trading.sessions.authenticate(
            api_key=broker_api_key,
            client_code=client_code,
            password=password
        )
        session_id = auth_resp.session_id
        print(f"✅ Credentials received! Session ID: {session_id}")
    except MintzyAuthError as e:
        print(f"❌ Mintzy Auth Failed. Check your API key. Error: {e}")
        return
    except MintzyError as e:
        print(f"❌ Broker Auth Failed: {e}")
        return

    print("\n2. TOTP Verification")
    totp_code = input("  Enter 6-digit TOTP code: ").strip()
    print("🔄 Verifying TOTP...")
    try:
        client.trading.sessions.verify_totp(session_id=session_id, totp=totp_code)
        print("✅ Authentication complete!")
    except MintzyError as e:
        print(f"❌ TOTP Verification Failed: {e}")
        return

    print("\n3. Trading Configuration (The 'Config Form')")
    ticker = input("  Enter Ticker (e.g., TCS): ").strip()
    strategy = input("  Enter Strategy Name (e.g., MACD_Crossover): ").strip()
    stop_loss = input("  Enter Stop Loss % (e.g., 2.5): ").strip()
    
    print("🔄 Saving configuration to backend...")
    try:
        config_resp = client.trading.configurations.create_configuration(
            name=f"{ticker} - {strategy}",
            configuration_data={
                "ticker": ticker,
                "strategy": strategy,
                "stop_loss_pct": float(stop_loss)
            }
        )
        config_id = config_resp.id
        print(f"✅ Configuration saved! Config ID: {config_id}")
    except MintzyError as e:
        print(f"❌ Failed to save configuration: {e}")
        return

    print("\n4. Start Trading")
    start = input("  Do you want to start live trading with this config? (y/n): ").strip().lower()
    if start == 'y':
        print("🔄 Sending start command to trading engine...")
        try:
            client.trading.sessions.start(session_id=session_id, configuration_id=config_id)
            print("✅ Trading Active! The engine is now running in the background.")
        except MintzyError as e:
            print(f"❌ Failed to start trading: {e}")
            return
        
        print("\n5. Live Dashboard & P&L Monitoring (Polling every 10 seconds, press Ctrl+C to stop)")
        try:
            for _ in range(3): # Poll 3 times for the sake of the test
                # Fetch live PnL
                pnl_resp = client.trading.pnl.get_live_pnl(session_id=session_id)
                # Fetch recent trades
                trades_resp = client.trading.sessions.get_trades(session_id=session_id)
                
                print("-" * 40)
                print(f"⏰ [{pnl_resp.timestamp}] LIVE DASHBOARD")
                print(f"💰 Realized PnL:   ₹{pnl_resp.current_pnl}")
                print(f"📈 Total Trades Executed: {len(trades_resp) if trades_resp else 0}")
                if trades_resp:
                    latest_trade = trades_resp[-1]
                    print(f"⚡ Last Action: {latest_trade.get('action')} {latest_trade.get('ticker')} @ {latest_trade.get('price')}")
                
                time.sleep(10)
        except KeyboardInterrupt:
            print("\n⏹️ Stopped monitoring.")
        except MintzyError as e:
            print(f"⚠️ Error fetching live data: {e}")
            
        print("\n6. Stop Trading")
        stop = input("  Do you want to stop trading and exit positions? (y/n): ").strip().lower()
        if stop == 'y':
            print("🔄 Stopping session...")
            try:
                client.trading.sessions.stop(session_id=session_id)
                print("✅ Trading stopped. Positions have been exited.")
            except MintzyError as e:
                print(f"❌ Failed to stop trading: {e}")
    else:
        print("\nSkipping start trading. Abandoning session.")
        try:
            client.trading.sessions.abandon(session_id=session_id)
            print("✅ Session abandoned.")
        except Exception:
            pass

    print("\nTest completed.")

if __name__ == "__main__":
    main()
