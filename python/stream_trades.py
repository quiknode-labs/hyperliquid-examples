#!/usr/bin/env python3
"""
WebSocket Streaming Example — Real-Time Market Data

Stream trades, orders, book updates, L2 book, and user data via WebSocket.
Includes all 20+ subscription types with automatic reconnection.

Setup:
    pip install hyperliquid-sdk

Usage:
    export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
    python stream_trades.py

The SDK handles:
- Automatic reconnection with exponential backoff
- Ping/pong heartbeats
- Connection state management
- Subscription resubscription on reconnect
"""

import os
import signal
import sys
import time
from datetime import datetime

from hyperliquid_sdk import Stream, ConnectionState

ENDPOINT = os.environ.get("ENDPOINT")
if not ENDPOINT:
    print("WebSocket Streaming Example")
    print("=" * 60)
    print()
    print("Usage:")
    print("  export ENDPOINT='https://YOUR-ENDPOINT.quiknode.pro/TOKEN'")
    print("  python stream_trades.py")
    sys.exit(1)


def timestamp():
    """Get current timestamp."""
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 1: Stream Trades
# ═══════════════════════════════════════════════════════════════════════════════

def stream_trades_example():
    """Stream real-time trades for BTC and ETH."""
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Streaming Trades")
    print("=" * 60)

    trade_count = 0

    def on_trade(data):
        nonlocal trade_count
        # Data format: {"channel": "trades", "data": [{trade}, ...]}
        trades = data.get("data", [])
        if isinstance(trades, list):
            for t in trades:
                trade_count += 1
                coin = t.get("coin", "?")
                px = float(t.get("px", 0))
                sz = t.get("sz", "?")
                side = "BUY " if t.get("side") == "B" else "SELL"
                print(f"[{timestamp()}] {side} {sz} {coin} @ ${px:,.2f}")

                if trade_count >= 5:
                    print(f"\nReceived {trade_count} trades. Moving to next example...")
                    return

    stream = Stream(ENDPOINT, reconnect=False)
    stream.trades(["BTC", "ETH"], on_trade)

    print("Subscribing to BTC and ETH trades...")
    print("-" * 60)

    stream.start()

    start = time.time()
    while trade_count < 5 and time.time() - start < 20:
        time.sleep(0.1)

    stream.stop()
    print(f"Total trades received: {trade_count}")


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 2: Stream L2 Order Book
# ═══════════════════════════════════════════════════════════════════════════════

def stream_l2_book_example():
    """Stream L2 order book snapshots."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Streaming L2 Order Book")
    print("=" * 60)
    print()
    print("L2 book shows aggregated order sizes at each price level.")
    print()

    update_count = 0

    def on_l2_book(data):
        nonlocal update_count
        update_count += 1

        # Data format: {"channel": "l2Book", "data": {coin, levels: [[bids], [asks]]}}
        book = data.get("data", {})
        coin = book.get("coin", "BTC")
        levels = book.get("levels", [[], []])

        bids = levels[0] if len(levels) > 0 else []
        asks = levels[1] if len(levels) > 1 else []

        if bids and asks:
            best_bid = bids[0] if bids else {}
            best_ask = asks[0] if asks else {}

            bid_px = float(best_bid.get("px", 0))
            bid_sz = best_bid.get("sz", "0")
            ask_px = float(best_ask.get("px", 0))
            ask_sz = best_ask.get("sz", "0")
            spread = ask_px - bid_px

            print(f"[{timestamp()}] {coin} L2 Book:")
            print(f"  Best Bid: ${bid_px:,.2f} x {bid_sz}")
            print(f"  Best Ask: ${ask_px:,.2f} x {ask_sz}")
            print(f"  Spread:   ${spread:,.2f}")
            print(f"  Levels:   {len(bids)} bids, {len(asks)} asks")
            print()

        if update_count >= 3:
            print("Received 3 L2 updates. Moving to next example...")

    stream = Stream(ENDPOINT, reconnect=False)
    stream.l2_book("BTC", on_l2_book)

    print("Subscribing to BTC L2 order book...")
    print("-" * 60)

    stream.start()

    start = time.time()
    while update_count < 3 and time.time() - start < 20:
        time.sleep(0.1)

    stream.stop()
    print(f"Total L2 updates received: {update_count}")


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 3: Stream Book Updates (Incremental)
# ═══════════════════════════════════════════════════════════════════════════════

def stream_book_updates_example():
    """Stream incremental book updates (deltas)."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Streaming Book Updates (Incremental)")
    print("=" * 60)
    print()
    print("Book updates show changes to the order book (deltas).")
    print("More efficient than full L2 snapshots for high-frequency use.")
    print()

    update_count = 0

    def on_book_update(data):
        nonlocal update_count
        update_count += 1

        book = data.get("data", {})
        coin = book.get("coin", "?")
        levels = book.get("levels", [[], []])

        bid_changes = len(levels[0]) if len(levels) > 0 else 0
        ask_changes = len(levels[1]) if len(levels) > 1 else 0

        print(f"[{timestamp()}] {coin} Book Update: {bid_changes} bid changes, {ask_changes} ask changes")

        if update_count >= 10:
            print(f"\nReceived {update_count} updates. Moving to next example...")

    stream = Stream(ENDPOINT, reconnect=False)
    stream.book_updates(["BTC"], on_book_update)

    print("Subscribing to BTC book updates...")
    print("-" * 60)

    stream.start()

    start = time.time()
    while update_count < 10 and time.time() - start < 20:
        time.sleep(0.1)

    stream.stop()
    print(f"Total book updates received: {update_count}")


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 4: Stream All Mid Prices
# ═══════════════════════════════════════════════════════════════════════════════

def stream_all_mids_example():
    """Stream all mid prices (efficient for monitoring many assets)."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Streaming All Mid Prices")
    print("=" * 60)
    print()
    print("Get real-time mid prices for ALL assets in one stream.")
    print()

    update_count = 0

    def on_all_mids(data):
        nonlocal update_count
        update_count += 1

        # Data format: {"channel": "allMids", "data": {"mids": {"BTC": "95000", "ETH": "3500", ...}}}
        mids_data = data.get("data", {})
        mids = mids_data.get("mids", mids_data)  # Handle both formats

        if isinstance(mids, dict):
            # Show top 5 by price
            sorted_mids = sorted(
                [(k, float(v)) for k, v in mids.items() if v],
                key=lambda x: x[1],
                reverse=True
            )[:5]

            print(f"[{timestamp()}] All Mids Update (top 5 by price):")
            for coin, price in sorted_mids:
                print(f"  {coin}: ${price:,.2f}")
            print()

        if update_count >= 3:
            print("Received 3 updates. Moving to next example...")

    stream = Stream(ENDPOINT, reconnect=False)
    stream.all_mids(on_all_mids)

    print("Subscribing to all mid prices...")
    print("-" * 60)

    stream.start()

    start = time.time()
    while update_count < 3 and time.time() - start < 20:
        time.sleep(0.1)

    stream.stop()
    print(f"Total mid price updates received: {update_count}")


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 5: Stream Candles
# ═══════════════════════════════════════════════════════════════════════════════

def stream_candles_example():
    """Stream candlestick data."""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Streaming Candles")
    print("=" * 60)
    print()
    print("Real-time candlestick updates.")
    print("Intervals: 1m, 5m, 15m, 1h, 4h, 1d")
    print()

    update_count = 0

    def on_candle(data):
        nonlocal update_count
        update_count += 1

        candle = data.get("data", {})
        coin = candle.get("s", "?")  # Symbol
        o = candle.get("o", "?")     # Open
        h = candle.get("h", "?")     # High
        l = candle.get("l", "?")     # Low
        c = candle.get("c", "?")     # Close
        v = candle.get("v", "?")     # Volume

        print(f"[{timestamp()}] {coin} 1m Candle:")
        print(f"  O: {o}  H: {h}  L: {l}  C: {c}  V: {v}")
        print()

        if update_count >= 2:
            print("Received 2 candle updates. Moving to next example...")

    stream = Stream(ENDPOINT, reconnect=False)
    stream.candle("BTC", "1m", on_candle)

    print("Subscribing to BTC 1-minute candles...")
    print("-" * 60)

    stream.start()

    start = time.time()
    while update_count < 2 and time.time() - start < 120:  # Candles update every minute
        time.sleep(0.1)

    stream.stop()
    print(f"Total candle updates received: {update_count}")


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 6: Stream BBO (Best Bid/Offer)
# ═══════════════════════════════════════════════════════════════════════════════

def stream_bbo_example():
    """Stream best bid/offer updates."""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Streaming BBO (Best Bid/Offer)")
    print("=" * 60)
    print()
    print("Efficient stream for just the top of book.")
    print()

    update_count = 0

    def on_bbo(data):
        nonlocal update_count
        update_count += 1

        bbo = data.get("data", {})
        coin = bbo.get("coin", "?")
        bid_px = bbo.get("bidPx", "?")
        bid_sz = bbo.get("bidSz", "?")
        ask_px = bbo.get("askPx", "?")
        ask_sz = bbo.get("askSz", "?")

        print(f"[{timestamp()}] {coin} BBO: Bid {bid_sz}@{bid_px} | Ask {ask_sz}@{ask_px}")

        if update_count >= 5:
            print(f"\nReceived {update_count} BBO updates. Demo complete!")

    stream = Stream(ENDPOINT, reconnect=False)
    stream.bbo("BTC", on_bbo)

    print("Subscribing to BTC BBO...")
    print("-" * 60)

    stream.start()

    start = time.time()
    while update_count < 5 and time.time() - start < 20:
        time.sleep(0.1)

    stream.stop()
    print(f"Total BBO updates received: {update_count}")


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 7: Multiple Subscriptions with Connection Management
# ═══════════════════════════════════════════════════════════════════════════════

def multi_stream_example():
    """Stream multiple data types with full connection management."""
    print("\n" + "=" * 60)
    print("EXAMPLE 7: Multiple Subscriptions + Connection Management")
    print("=" * 60)

    counts = {"trades": 0, "l2": 0, "mids": 0}

    def on_trade(data):
        counts["trades"] += 1
        trades = data.get("data", [])
        if isinstance(trades, list) and trades:
            coin = trades[0].get("coin", "?")
            print(f"[TRADE] {coin} - Total: {counts['trades']}")

    def on_l2(data):
        counts["l2"] += 1
        book = data.get("data", {})
        coin = book.get("coin", "?")
        print(f"[L2]    {coin} - Total: {counts['l2']}")

    def on_mids(data):
        counts["mids"] += 1
        print(f"[MIDS]  All assets - Total: {counts['mids']}")

    def on_state(state: ConnectionState):
        print(f"[STATE] {state.value}")

    def on_open():
        print("[CONNECTED] WebSocket ready")

    def on_error(error):
        print(f"[ERROR] {error}")

    stream = Stream(
        ENDPOINT,
        on_error=on_error,
        on_open=on_open,
        on_state_change=on_state,
        reconnect=True,
        max_reconnect_attempts=3,
    )

    # Multiple subscriptions
    stream.trades(["BTC", "ETH"], on_trade)
    stream.l2_book("BTC", on_l2)
    stream.all_mids(on_mids)

    print("Subscribing to trades, L2 book, and all mids...")
    print("-" * 60)

    def signal_handler(sig, frame):
        print("\nStopping...")
        stream.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    stream.start()

    # Run for 15 seconds
    time.sleep(15)

    stream.stop()

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Trades received: {counts['trades']}")
    print(f"  L2 updates:      {counts['l2']}")
    print(f"  Mid updates:     {counts['mids']}")


# ═══════════════════════════════════════════════════════════════════════════════
# USER DATA STREAMS (Requires user address)
# ═══════════════════════════════════════════════════════════════════════════════

def user_streams_info():
    """Show available user data streams."""
    print("\n" + "=" * 60)
    print("USER DATA STREAMS")
    print("=" * 60)
    print()
    print("The following streams require a user address:")
    print()
    print("  stream.open_orders(user, callback)")
    print("    - User's open orders")
    print()
    print("  stream.order_updates(user, callback)")
    print("    - Order status changes")
    print()
    print("  stream.user_events(user, callback)")
    print("    - All user events (fills, funding, liquidations)")
    print()
    print("  stream.user_fills(user, callback)")
    print("    - Trade fills")
    print()
    print("  stream.user_fundings(user, callback)")
    print("    - Funding payments")
    print()
    print("  stream.user_non_funding_ledger(user, callback)")
    print("    - Ledger changes (deposits, withdrawals, transfers)")
    print()
    print("  stream.clearinghouse_state(user, callback)")
    print("    - Position and margin updates")
    print()
    print("  stream.active_asset_data(user, coin, callback)")
    print("    - User's trading parameters for specific asset")
    print()
    print("  stream.twap_states(user, callback)")
    print("    - TWAP algorithm states")
    print()
    print("  stream.user_twap_slice_fills(user, callback)")
    print("    - Individual TWAP order slice fills")
    print()
    print("  stream.user_twap_history(user, callback)")
    print("    - TWAP execution history")
    print()
    print("  stream.notification(user, callback)")
    print("    - User notifications")
    print()
    print("  stream.web_data_3(user, callback)")
    print("    - Aggregate user info for frontend use")
    print()
    print("Example:")
    print("  USER = '0x...'")
    print("  stream.user_fills(USER, lambda f: print(f'Fill: {f}'))")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("WebSocket Streaming Examples")
    print("=" * 60)
    print(f"Endpoint: {ENDPOINT[:50]}...")
    print()
    print("This demo shows WebSocket streaming capabilities:")
    print("  1. Trades — Real-time executed trades")
    print("  2. L2 Book — Order book snapshots")
    print("  3. Book Updates — Incremental order book changes")
    print("  4. All Mids — All asset mid prices")
    print("  5. Candles — Candlestick data")
    print("  6. BBO — Best bid/offer")
    print("  7. Multi-stream — Multiple subscriptions")
    print()

    try:
        stream_trades_example()
        stream_l2_book_example()
        stream_book_updates_example()
        stream_all_mids_example()
        # stream_candles_example()  # Takes ~1 min, uncomment to test
        stream_bbo_example()
        # multi_stream_example()  # Uncomment for full demo

        # Show user data streams info
        user_streams_info()

        print("=" * 60)
        print("All examples completed!")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\nDemo interrupted.")
    except Exception as e:
        print(f"\nError: {e}")
        raise
