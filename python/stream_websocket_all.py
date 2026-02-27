#!/usr/bin/env python3
"""
WebSocket Streaming — Complete Reference

This example demonstrates ALL WebSocket subscription types:
- Market Data: trades, l2_book, book_updates, all_mids, candle, bbo
- User Data: open_orders, user_fills, user_fundings, clearinghouse_state
- TWAP: twap, twap_states, user_twap_slice_fills
- System: events, notification

Setup:
    pip install hyperliquid-sdk

Usage:
    export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
    python stream_websocket_all.py
"""

import os
import signal
import sys
import time
from datetime import datetime
from typing import Dict, Any

from hyperliquid_sdk import Stream, ConnectionState

ENDPOINT = os.environ.get("ENDPOINT")
USER = os.environ.get("USER_ADDRESS", "0x0000000000000000000000000000000000000000")

if not ENDPOINT:
    print("WebSocket Complete Reference")
    print("=" * 60)
    print()
    print("Usage:")
    print("  export ENDPOINT='https://YOUR-ENDPOINT.quiknode.pro/TOKEN'")
    print("  export USER_ADDRESS='0x...'  # Optional, for user data streams")
    print("  python stream_websocket_all.py")
    sys.exit(1)


def timestamp():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


# Global counters
counts: Dict[str, int] = {}


def make_callback(name: str, max_prints: int = 3):
    """Create a callback that prints first N messages."""
    counts[name] = 0

    def callback(data: Dict[str, Any]):
        counts[name] += 1
        if counts[name] <= max_prints:
            channel = data.get("channel", "unknown")
            print(f"[{timestamp()}] {name.upper()}: {channel} (#{counts[name]})")
            # Print first few fields of data
            inner_data = data.get("data", data)
            if isinstance(inner_data, dict):
                keys = list(inner_data.keys())[:3]
                print(f"             Fields: {keys}")
            elif isinstance(inner_data, list) and inner_data:
                print(f"             Items: {len(inner_data)}")

    return callback


# ═══════════════════════════════════════════════════════════════════════════════
# MARKET DATA STREAMS
# ═══════════════════════════════════════════════════════════════════════════════

def demo_market_data():
    """Demo all market data streams."""
    print("\n" + "=" * 60)
    print("MARKET DATA STREAMS")
    print("=" * 60)
    print()
    print("Available streams:")
    print("  - trades(coins, callback)")
    print("  - book_updates(coins, callback)")
    print("  - l2_book(coin, callback)")
    print("  - all_mids(callback)")
    print("  - candle(coin, interval, callback)")
    print("  - bbo(coin, callback)")
    print("  - active_asset_ctx(coin, callback)")
    print()

    stream = Stream(ENDPOINT, reconnect=False)

    # trades: Real-time executed trades
    stream.trades(["BTC", "ETH"], make_callback("trades"))

    # book_updates: Incremental order book changes
    stream.book_updates(["BTC"], make_callback("book_updates"))

    # l2_book: Full L2 order book snapshots
    stream.l2_book("BTC", make_callback("l2_book"))

    # all_mids: All asset mid prices
    stream.all_mids(make_callback("all_mids"))

    # bbo: Best bid/offer updates
    stream.bbo("ETH", make_callback("bbo"))

    # active_asset_ctx: Asset context (funding, OI, volume)
    stream.active_asset_ctx("BTC", make_callback("asset_ctx"))

    print("Subscribing to market data streams...")
    print("-" * 60)

    stream.start()

    # Wait for messages
    time.sleep(10)

    stream.stop()

    print()
    print("Market data summary:")
    for name in ["trades", "book_updates", "l2_book", "all_mids", "bbo", "asset_ctx"]:
        print(f"  {name}: {counts.get(name, 0)} messages")


# ═══════════════════════════════════════════════════════════════════════════════
# USER DATA STREAMS (requires user address)
# ═══════════════════════════════════════════════════════════════════════════════

def demo_user_data():
    """Demo user data streams."""
    print("\n" + "=" * 60)
    print("USER DATA STREAMS")
    print("=" * 60)
    print()
    print(f"User address: {USER}")
    print()
    print("Available streams:")
    print("  - orders(coins, callback, users=[...])")
    print("  - open_orders(user, callback)")
    print("  - order_updates(user, callback)")
    print("  - user_events(user, callback)")
    print("  - user_fills(user, callback)")
    print("  - user_fundings(user, callback)")
    print("  - user_non_funding_ledger(user, callback)")
    print("  - clearinghouse_state(user, callback)")
    print("  - active_asset_data(user, coin, callback)")
    print()

    if USER == "0x0000000000000000000000000000000000000000":
        print("NOTE: Set USER_ADDRESS env var for real user data.")
        print("      Skipping user data demo.")
        return

    stream = Stream(ENDPOINT, reconnect=False)

    # orders: Order lifecycle for specific user
    stream.orders(["BTC", "ETH"], make_callback("orders"), users=[USER])

    # open_orders: User's open orders
    stream.open_orders(USER, make_callback("open_orders"))

    # user_fills: Trade fills
    stream.user_fills(USER, make_callback("user_fills"))

    # user_fundings: Funding payments
    stream.user_fundings(USER, make_callback("user_fundings"))

    # clearinghouse_state: Positions and margin
    stream.clearinghouse_state(USER, make_callback("clearinghouse"))

    print("Subscribing to user data streams...")
    print("-" * 60)

    stream.start()

    time.sleep(10)

    stream.stop()

    print()
    print("User data summary:")
    for name in ["orders", "open_orders", "user_fills", "user_fundings", "clearinghouse"]:
        print(f"  {name}: {counts.get(name, 0)} messages")


# ═══════════════════════════════════════════════════════════════════════════════
# TWAP STREAMS
# ═══════════════════════════════════════════════════════════════════════════════

def demo_twap():
    """Demo TWAP streams."""
    print("\n" + "=" * 60)
    print("TWAP STREAMS")
    print("=" * 60)
    print()
    print("Available streams:")
    print("  - twap(coins, callback)")
    print("  - twap_states(user, callback)")
    print("  - user_twap_slice_fills(user, callback)")
    print("  - user_twap_history(user, callback)")
    print()

    stream = Stream(ENDPOINT, reconnect=False)

    # twap: TWAP execution updates
    stream.twap(["BTC", "ETH"], make_callback("twap"))

    print("Subscribing to TWAP streams...")
    print("-" * 60)

    stream.start()

    time.sleep(5)

    stream.stop()

    print()
    print("TWAP summary:")
    print(f"  twap: {counts.get('twap', 0)} messages")


# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM STREAMS
# ═══════════════════════════════════════════════════════════════════════════════

def demo_system():
    """Demo system streams."""
    print("\n" + "=" * 60)
    print("SYSTEM STREAMS")
    print("=" * 60)
    print()
    print("Available streams:")
    print("  - events(callback)")
    print("  - writer_actions(callback)")
    print("  - notification(user, callback)")
    print("  - web_data_3(user, callback)")
    print()

    stream = Stream(ENDPOINT, reconnect=False)

    # events: System events (funding, liquidations)
    stream.events(make_callback("events"))

    # writer_actions: Spot token transfers
    stream.writer_actions(make_callback("writer_actions"))

    print("Subscribing to system streams...")
    print("-" * 60)

    stream.start()

    time.sleep(5)

    stream.stop()

    print()
    print("System summary:")
    for name in ["events", "writer_actions"]:
        print(f"  {name}: {counts.get(name, 0)} messages")


# ═══════════════════════════════════════════════════════════════════════════════
# CONNECTION MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

def demo_connection_management():
    """Demo connection callbacks and management."""
    print("\n" + "=" * 60)
    print("CONNECTION MANAGEMENT")
    print("=" * 60)
    print()
    print("Available callbacks:")
    print("  - on_open: Called when connected")
    print("  - on_close: Called when disconnected")
    print("  - on_error: Called on errors")
    print("  - on_reconnect: Called on reconnection")
    print("  - on_state_change: Called on state changes")
    print()
    print("Properties:")
    print("  - stream.connected: bool")
    print("  - stream.state: ConnectionState")
    print("  - stream.reconnect_attempts: int")
    print()

    def on_open():
        print(f"[{timestamp()}] CONNECTED")

    def on_close():
        print(f"[{timestamp()}] CLOSED")

    def on_error(error):
        print(f"[{timestamp()}] ERROR: {error}")

    def on_state_change(state: ConnectionState):
        print(f"[{timestamp()}] STATE: {state.value}")

    stream = Stream(
        ENDPOINT,
        on_open=on_open,
        on_close=on_close,
        on_error=on_error,
        on_state_change=on_state_change,
        reconnect=True,
        max_reconnect_attempts=3,
    )

    stream.trades(["BTC"], make_callback("conn_test"))

    print("Testing connection management...")
    print("-" * 60)

    stream.start()

    print(f"  Connected: {stream.connected}")
    print(f"  State: {stream.state.value}")

    time.sleep(5)

    stream.stop()

    print(f"\n  Final state: {stream.state.value}")


# ═══════════════════════════════════════════════════════════════════════════════
# REFERENCE TABLE
# ═══════════════════════════════════════════════════════════════════════════════

def print_reference():
    """Print complete reference table."""
    print("\n" + "=" * 60)
    print("WEBSOCKET SUBSCRIPTION REFERENCE")
    print("=" * 60)
    print()
    print("┌────────────────────────┬────────────────────────────────────────┐")
    print("│ Method                 │ Description                            │")
    print("├────────────────────────┼────────────────────────────────────────┤")
    print("│ MARKET DATA            │                                        │")
    print("│ trades(coins, cb)      │ Executed trades                        │")
    print("│ book_updates(coins,cb) │ Order book deltas                      │")
    print("│ l2_book(coin, cb)      │ Full L2 order book                     │")
    print("│ all_mids(cb)           │ All asset mid prices                   │")
    print("│ candle(coin,int,cb)    │ OHLCV candles (1m,5m,15m,1h,4h,1d)     │")
    print("│ bbo(coin, cb)          │ Best bid/offer                         │")
    print("│ active_asset_ctx(c,cb) │ Asset context (funding, OI)            │")
    print("├────────────────────────┼────────────────────────────────────────┤")
    print("│ USER DATA              │                                        │")
    print("│ orders(coins,cb,users) │ Order lifecycle (filtered)             │")
    print("│ open_orders(user, cb)  │ User's open orders                     │")
    print("│ order_updates(user,cb) │ Order status changes                   │")
    print("│ user_events(user, cb)  │ All user events                        │")
    print("│ user_fills(user, cb)   │ Trade fills                            │")
    print("│ user_fundings(user,cb) │ Funding payments                       │")
    print("│ user_non_fund..(u,cb)  │ Ledger updates                         │")
    print("│ clearinghouse..(u,cb)  │ Positions/margin                       │")
    print("│ active_asset..(u,c,cb) │ User trading params                    │")
    print("├────────────────────────┼────────────────────────────────────────┤")
    print("│ TWAP                   │                                        │")
    print("│ twap(coins, cb)        │ TWAP execution                         │")
    print("│ twap_states(user, cb)  │ TWAP algorithm states                  │")
    print("│ user_twap_slice..(u,c) │ TWAP slice fills                       │")
    print("│ user_twap_hist..(u,cb) │ TWAP history                           │")
    print("├────────────────────────┼────────────────────────────────────────┤")
    print("│ SYSTEM                 │                                        │")
    print("│ events(cb)             │ Funding, liquidations                  │")
    print("│ writer_actions(cb)     │ Spot token transfers                   │")
    print("│ notification(user,cb)  │ User notifications                     │")
    print("│ web_data_3(user, cb)   │ Aggregate user info                    │")
    print("└────────────────────────┴────────────────────────────────────────┘")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("WebSocket Streaming — Complete Reference")
    print("=" * 60)
    print(f"Endpoint: {ENDPOINT[:50]}...")
    print()

    # Handle Ctrl+C
    def signal_handler(sig, frame):
        print("\nDemo interrupted.")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    try:
        # Print reference table
        print_reference()

        # Run demos
        demo_market_data()
        demo_user_data()
        demo_twap()
        demo_system()
        demo_connection_management()

        print()
        print("=" * 60)
        print("All WebSocket examples completed!")
        print("=" * 60)
        print()
        print("Total messages received:")
        for name, count in sorted(counts.items()):
            print(f"  {name}: {count}")

    except KeyboardInterrupt:
        print("\nDemo interrupted.")
    except Exception as e:
        print(f"\nError: {e}")
        raise
