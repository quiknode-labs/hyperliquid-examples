#!/usr/bin/env python3
"""
WebSocket Streaming Example — Real-Time HyperCore Data

Stream trades, orders, book updates, events, and TWAP via WebSocket.
These are the data streams available on QuickNode endpoints.

Available QuickNode WebSocket streams:
- trades: Executed trades with price, size, direction
- orders: Order lifecycle events (open, filled, cancelled)
- book_updates: Order book changes (incremental deltas)
- events: Balance changes, transfers, deposits, withdrawals
- twap: TWAP execution data
- writer_actions: HyperCore <-> HyperEVM asset transfers

Note: L2/L4 order book snapshots are available via gRPC (see stream_orderbook.py).
      Other streams (allMids, bbo, candle) require the public Hyperliquid API.

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
        # QuickNode format: {"type": "data", "stream": "hl.trades", "block": {"events": [...]}}
        # Events are [[user, trade_data], ...]
        block = data.get("block", {})
        for event in block.get("events", []):
            if isinstance(event, list) and len(event) >= 2:
                t = event[1]  # trade_data is second element
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
# EXAMPLE 2: Stream Orders
# ═══════════════════════════════════════════════════════════════════════════════

def stream_orders_example():
    """Stream order lifecycle events."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Streaming Orders")
    print("=" * 60)
    print()
    print("Order events: open, filled, triggered, canceled, etc.")
    print()

    order_count = 0

    def on_order(data):
        nonlocal order_count
        block = data.get("block", {})
        for event in block.get("events", []):
            if isinstance(event, list) and len(event) >= 2:
                o = event[1]  # order data
                order_count += 1
                coin = o.get("coin", "?")
                status = o.get("status", "?")
                side = "BUY" if o.get("side") == "B" else "SELL"
                px = o.get("px", "?")
                sz = o.get("sz", "?")
                print(f"[{timestamp()}] {status}: {side} {sz} {coin} @ ${px}")

                if order_count >= 10:
                    print(f"\nReceived {order_count} orders. Moving to next example...")
                    return

    stream = Stream(ENDPOINT, reconnect=False)
    stream.orders(["BTC", "ETH"], on_order)

    print("Subscribing to BTC and ETH orders...")
    print("-" * 60)

    stream.start()

    start = time.time()
    while order_count < 10 and time.time() - start < 20:
        time.sleep(0.1)

    stream.stop()
    print(f"Total orders received: {order_count}")


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 3: Stream Book Updates (Incremental)
# ═══════════════════════════════════════════════════════════════════════════════

def stream_book_updates_example():
    """Stream incremental book updates (deltas)."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Streaming Book Updates (Incremental)")
    print("=" * 60)
    print()
    print("Book updates show individual order changes to the order book.")
    print("Each event contains: user, oid, coin, side, px, raw_book_diff")
    print()

    update_count = 0

    def on_book_update(data):
        nonlocal update_count
        block = data.get("block", {})
        events = block.get("events", [])

        if events:
            update_count += 1
            # Show first event from this block
            event = events[0]
            coin = event.get("coin", "?")
            side = "BID" if event.get("side") == "B" else "ASK"
            px = event.get("px", "?")
            diff = event.get("raw_book_diff", {})

            if diff == "remove":
                action = "REMOVE"
                sz = "-"
            else:
                action = "ADD/UPDATE"
                sz = diff.get("new", {}).get("sz", "?") if isinstance(diff, dict) else "?"

            print(f"[{timestamp()}] {coin} {side} @ ${px}: {action} size={sz} (+{len(events)-1} more)")

            if update_count >= 10:
                print(f"\nReceived {update_count} blocks. Moving to next example...")

    stream = Stream(ENDPOINT, reconnect=False)
    stream.book_updates(["BTC"], on_book_update)

    print("Subscribing to BTC book updates...")
    print("-" * 60)

    stream.start()

    start = time.time()
    while update_count < 10 and time.time() - start < 20:
        time.sleep(0.1)

    stream.stop()
    print(f"Total book update blocks received: {update_count}")


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 4: Stream Events
# ═══════════════════════════════════════════════════════════════════════════════

def stream_events_example():
    """Stream balance changes, transfers, deposits, withdrawals."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Streaming Events")
    print("=" * 60)
    print()
    print("Events: balance changes, transfers, deposits, withdrawals, vault ops")
    print()

    event_count = 0

    def on_event(data):
        nonlocal event_count
        block = data.get("block", {})
        events = block.get("events", [])

        for event in events:
            event_count += 1
            # Event structure varies by type
            event_type = "unknown"
            if isinstance(event, dict):
                if "deposit" in event:
                    event_type = "deposit"
                elif "withdraw" in event:
                    event_type = "withdraw"
                elif "transfer" in event:
                    event_type = "transfer"
                elif "funding" in event:
                    event_type = "funding"
                elif "liquidation" in event:
                    event_type = "liquidation"
                else:
                    event_type = list(event.keys())[0] if event else "unknown"

            print(f"[{timestamp()}] Event #{event_count}: {event_type}")

            if event_count >= 5:
                print(f"\nReceived {event_count} events. Moving to next example...")
                return

    stream = Stream(ENDPOINT, reconnect=False)
    stream.events(on_event)

    print("Subscribing to all events...")
    print("-" * 60)

    stream.start()

    start = time.time()
    while event_count < 5 and time.time() - start < 30:
        time.sleep(0.1)

    stream.stop()
    print(f"Total events received: {event_count}")


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 5: Multiple Subscriptions with Connection Management
# ═══════════════════════════════════════════════════════════════════════════════

def multi_stream_example():
    """Stream multiple data types with full connection management."""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Multiple Subscriptions + Connection Management")
    print("=" * 60)

    counts = {"trades": 0, "orders": 0, "book": 0}

    def on_trade(data):
        counts["trades"] += 1
        block = data.get("block", {})
        events = block.get("events", [])
        if events and isinstance(events[0], list) and len(events[0]) >= 2:
            coin = events[0][1].get("coin", "?")
            print(f"[TRADE] {coin} - Total: {counts['trades']}")

    def on_order(data):
        counts["orders"] += 1
        block = data.get("block", {})
        events = block.get("events", [])
        if events and isinstance(events[0], list) and len(events[0]) >= 2:
            coin = events[0][1].get("coin", "?")
            status = events[0][1].get("status", "?")
            print(f"[ORDER] {coin} {status} - Total: {counts['orders']}")

    def on_book(data):
        counts["book"] += 1
        block = data.get("block", {})
        events = block.get("events", [])
        if events:
            coin = events[0].get("coin", "?")
            print(f"[BOOK]  {coin} changes: {len(events)} - Total blocks: {counts['book']}")

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

    # Multiple subscriptions (all QuickNode-supported)
    stream.trades(["BTC", "ETH"], on_trade)
    stream.orders(["BTC"], on_order)
    stream.book_updates(["BTC"], on_book)

    print("Subscribing to trades, orders, and book updates...")
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
    print(f"  Trades received:     {counts['trades']}")
    print(f"  Orders received:     {counts['orders']}")
    print(f"  Book update blocks:  {counts['book']}")


# ═══════════════════════════════════════════════════════════════════════════════
# AVAILABLE STREAMS INFO
# ═══════════════════════════════════════════════════════════════════════════════

def streams_info():
    """Show available QuickNode WebSocket streams."""
    print("\n" + "=" * 60)
    print("AVAILABLE QUICKNODE WEBSOCKET STREAMS")
    print("=" * 60)
    print()
    print("HyperCore Data Streams:")
    print()
    print("  stream.trades(coins, callback)")
    print("    - Executed trades with price, size, direction")
    print()
    print("  stream.orders(coins, callback)")
    print("    - Order lifecycle: open, filled, triggered, canceled")
    print()
    print("  stream.book_updates(coins, callback)")
    print("    - Incremental order book changes (deltas)")
    print()
    print("  stream.events(callback)")
    print("    - Balance changes, transfers, deposits, withdrawals")
    print()
    print("  stream.twap(coins, callback)")
    print("    - TWAP execution data and progress")
    print()
    print("  stream.writer_actions(callback)")
    print("    - HyperCore <-> HyperEVM asset transfers")
    print()
    print("For L2/L4 Order Books:")
    print("  Use gRPC streaming (see stream_orderbook.py)")
    print("  - StreamL2Book: Aggregated price levels")
    print("  - StreamL4Book: Individual orders with order IDs")
    print()
    print("Example with filtering:")
    print("  stream.trades(['BTC', 'ETH'], lambda t: print(t))")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("WebSocket Streaming Examples (QuickNode)")
    print("=" * 60)
    print(f"Endpoint: {ENDPOINT[:50]}...")
    print()
    print("This demo shows QuickNode WebSocket streaming capabilities:")
    print("  1. Trades - Real-time executed trades")
    print("  2. Orders - Order lifecycle events")
    print("  3. Book Updates - Incremental order book changes")
    print("  4. Events - Balance changes, transfers, etc.")
    print("  5. Multi-stream - Multiple subscriptions")
    print()

    try:
        stream_trades_example()
        stream_orders_example()
        stream_book_updates_example()
        stream_events_example()
        # multi_stream_example()  # Uncomment for full demo

        # Show available streams info
        streams_info()

        print("=" * 60)
        print("All examples completed!")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\nDemo interrupted.")
    except Exception as e:
        print(f"\nError: {e}")
        raise
