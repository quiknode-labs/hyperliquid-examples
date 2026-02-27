#!/usr/bin/env python3
"""
gRPC Streaming Example — High-Performance Real-Time Data

Stream trades, orders, L2 book, L4 book, and blocks via gRPC.
gRPC provides lower latency than WebSocket for high-frequency trading.

gRPC is included with all QuickNode Hyperliquid endpoints — no add-on needed.

Setup:
    pip install hyperliquid-sdk

Usage:
    export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
    python stream_grpc.py

The SDK:
- Connects to port 10000 automatically
- Passes token via x-token header
- Handles reconnection with exponential backoff
- Manages keepalive pings
"""

import os
import signal
import sys
import time
from datetime import datetime

from hyperliquid_sdk import GRPCStream, ConnectionState

ENDPOINT = os.environ.get("ENDPOINT")
if not ENDPOINT:
    print("gRPC Streaming Example")
    print("=" * 60)
    print()
    print("Usage:")
    print("  export ENDPOINT='https://YOUR-ENDPOINT.quiknode.pro/TOKEN'")
    print("  python stream_grpc.py")
    print()
    print("gRPC is included with all QuickNode Hyperliquid endpoints.")
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
        trade_count += 1
        coin = data.get("coin", "?")
        px = float(data.get("px", 0))
        sz = data.get("sz", "?")
        side = "BUY " if data.get("side") == "B" else "SELL"
        print(f"[{timestamp()}] {side} {sz} {coin} @ ${px:,.2f}")

        # Stop after 5 trades for demo
        if trade_count >= 5:
            print(f"\nReceived {trade_count} trades. Moving to next example...")

    stream = GRPCStream(ENDPOINT, reconnect=False)
    stream.trades(["BTC", "ETH"], on_trade)

    print("Subscribing to BTC and ETH trades...")
    print("-" * 60)

    stream.start()

    # Wait for trades or timeout
    start = time.time()
    while trade_count < 5 and time.time() - start < 15:
        time.sleep(0.1)

    stream.stop()
    print(f"Total trades received: {trade_count}")


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 2: Stream L2 Order Book (Aggregated Price Levels)
# ═══════════════════════════════════════════════════════════════════════════════

def stream_l2_book_example():
    """Stream L2 order book (aggregated by price level)."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Streaming L2 Order Book (Aggregated)")
    print("=" * 60)
    print()
    print("L2 book aggregates orders at each price level.")
    print("Use n_sig_figs to control price aggregation precision.")
    print()

    update_count = 0

    def on_l2_book(data):
        nonlocal update_count
        update_count += 1

        # L2 book structure: {coin, bids: [[px, sz], ...], asks: [[px, sz], ...]}
        coin = data.get("coin", "BTC")
        bids = data.get("bids", [])
        asks = data.get("asks", [])

        if bids and asks:
            best_bid = bids[0] if bids else ["N/A", "N/A"]
            best_ask = asks[0] if asks else ["N/A", "N/A"]

            bid_px = float(best_bid[0]) if best_bid[0] != "N/A" else 0
            ask_px = float(best_ask[0]) if best_ask[0] != "N/A" else 0
            spread = ask_px - bid_px if bid_px and ask_px else 0

            print(f"[{timestamp()}] {coin} L2 Book:")
            print(f"  Best Bid: ${bid_px:,.2f} x {best_bid[1]}")
            print(f"  Best Ask: ${ask_px:,.2f} x {best_ask[1]}")
            print(f"  Spread:   ${spread:,.2f}")
            print(f"  Levels:   {len(bids)} bids, {len(asks)} asks")
            print()

        if update_count >= 3:
            print("Received 3 L2 updates. Moving to next example...")

    stream = GRPCStream(ENDPOINT, reconnect=False)

    # n_sig_figs controls price aggregation:
    # - None or 5: Full precision
    # - 4: Aggregate to 4 significant figures
    # - 3: More aggregation (fewer levels, larger sizes)
    stream.l2_book("BTC", on_l2_book, n_sig_figs=5)

    print("Subscribing to BTC L2 order book...")
    print("-" * 60)

    stream.start()

    start = time.time()
    while update_count < 3 and time.time() - start < 15:
        time.sleep(0.1)

    stream.stop()
    print(f"Total L2 updates received: {update_count}")


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 3: Stream L4 Order Book (Individual Orders) — CRITICAL FOR TRADING
# ═══════════════════════════════════════════════════════════════════════════════

def stream_l4_book_example():
    """Stream L4 order book (individual orders).

    L4 book is CRITICAL for:
    - Market making: See exact order sizes and queue position
    - Order flow analysis: Detect large orders and icebergs
    - Optimal execution: Know exactly what you're crossing
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Streaming L4 Order Book (Individual Orders)")
    print("=" * 60)
    print()
    print("L4 book shows EVERY individual order in the book.")
    print("This is critical for market making and order flow analysis.")
    print()

    update_count = 0

    def on_l4_book(data):
        nonlocal update_count
        update_count += 1

        # L4 data has two types: "snapshot" or "diff"
        update_type = data.get("type", "unknown")
        coin = data.get("coin", "BTC")
        bids = data.get("bids", [])
        asks = data.get("asks", [])

        print(f"[{timestamp()}] {coin} L4 Book ({update_type}) #{update_count}:")

        if update_type == "snapshot":
            # Snapshot: bids/asks are lists of order dicts with limit_px, sz, oid, etc.
            print(f"  Total: {len(bids)} bids, {len(asks)} asks")
            print("  TOP BIDS:")
            for i, bid in enumerate(bids[:3]):
                if isinstance(bid, dict):
                    px = bid.get("limit_px", "?")
                    sz = bid.get("sz", "?")
                    oid = bid.get("oid", "?")
                    print(f"    [{i+1}] ${float(px):,.2f} x {sz} (oid: {oid})")

            print("  TOP ASKS:")
            for i, ask in enumerate(asks[:3]):
                if isinstance(ask, dict):
                    px = ask.get("limit_px", "?")
                    sz = ask.get("sz", "?")
                    oid = ask.get("oid", "?")
                    print(f"    [{i+1}] ${float(px):,.2f} x {sz} (oid: {oid})")
        else:
            # Diff: contains incremental changes
            diff_data = data.get("data", {})
            if diff_data:
                print(f"  Changes: {list(diff_data.keys())[:5]}...")
            else:
                print("  (incremental update)")

        print()

        if update_count >= 3:
            print("Received 3 L4 updates. Moving to next example...")

    stream = GRPCStream(ENDPOINT, reconnect=False)
    stream.l4_book("BTC", on_l4_book)

    print("Subscribing to BTC L4 order book (individual orders)...")
    print("-" * 60)

    stream.start()

    start = time.time()
    while update_count < 3 and time.time() - start < 15:
        time.sleep(0.1)

    stream.stop()
    print(f"Total L4 updates received: {update_count}")


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 4: Stream Orders (Order Lifecycle Events)
# ═══════════════════════════════════════════════════════════════════════════════

def stream_orders_example():
    """Stream order lifecycle events."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Streaming Order Events")
    print("=" * 60)
    print()
    print("Order events: open, filled, partially_filled, canceled, triggered")
    print()

    order_count = 0

    def on_order(data):
        nonlocal order_count
        order_count += 1

        coin = data.get("coin", "?")
        status = data.get("status", "?")
        side = "BUY " if data.get("side") == "B" else "SELL"
        px = data.get("px", "?")
        sz = data.get("sz", "?")
        oid = data.get("oid", "?")

        print(f"[{timestamp()}] ORDER {status.upper()}: {side} {sz} {coin} @ {px} (oid: {oid})")

        if order_count >= 5:
            print(f"\nReceived {order_count} order events. Moving to next example...")

    stream = GRPCStream(ENDPOINT, reconnect=False)

    # Can filter by specific users (optional)
    # stream.orders(["BTC", "ETH"], on_order, users=["0x..."])
    stream.orders(["BTC", "ETH"], on_order)

    print("Subscribing to BTC and ETH order events...")
    print("-" * 60)

    stream.start()

    start = time.time()
    while order_count < 5 and time.time() - start < 15:
        time.sleep(0.1)

    stream.stop()
    print(f"Total order events received: {order_count}")


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 5: Stream Blocks
# ═══════════════════════════════════════════════════════════════════════════════

def stream_blocks_example():
    """Stream block data."""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Streaming Blocks")
    print("=" * 60)

    block_count = 0

    def on_block(data):
        nonlocal block_count
        block_count += 1

        # Block structure: {"abci_block": {"time": "...", "signed_action_bundles": [...]}, "resps": [...]}
        abci_block = data.get("abci_block", {})
        block_time = abci_block.get("time", "?")
        bundles = len(abci_block.get("signed_action_bundles", []))

        print(f"[{timestamp()}] BLOCK @ {block_time} ({bundles} bundles)")

        if block_count >= 3:
            print(f"\nReceived {block_count} blocks. Demo complete!")

    stream = GRPCStream(ENDPOINT, reconnect=False)
    stream.blocks(on_block)

    print("Subscribing to blocks...")
    print("-" * 60)

    stream.start()

    start = time.time()
    while block_count < 3 and time.time() - start < 30:
        time.sleep(0.1)

    stream.stop()
    print(f"Total blocks received: {block_count}")


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE 6: Multiple Subscriptions with Connection Management
# ═══════════════════════════════════════════════════════════════════════════════

def multi_stream_example():
    """Stream multiple data types with full connection management."""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Multiple Subscriptions + Connection Management")
    print("=" * 60)

    counts = {"trades": 0, "l2": 0, "orders": 0}

    def on_trade(data):
        counts["trades"] += 1
        coin = data.get("coin", "?")
        print(f"[TRADE] {coin} - Total: {counts['trades']}")

    def on_l2(data):
        counts["l2"] += 1
        coin = data.get("coin", "?")
        print(f"[L2]    {coin} - Total: {counts['l2']}")

    def on_order(data):
        counts["orders"] += 1
        status = data.get("status", "?")
        print(f"[ORDER] {status} - Total: {counts['orders']}")

    def on_state(state: ConnectionState):
        print(f"[STATE] {state.value}")

    def on_connect():
        print("[CONNECTED] All streams active")

    def on_error(error):
        print(f"[ERROR] {error}")

    stream = GRPCStream(
        ENDPOINT,
        on_error=on_error,
        on_connect=on_connect,
        on_state_change=on_state,
        reconnect=True,
        max_reconnect_attempts=3,
    )

    # Chain multiple subscriptions
    stream.trades(["BTC"], on_trade)
    stream.l2_book("ETH", on_l2)
    stream.orders(["BTC", "ETH"], on_order)

    print("Subscribing to BTC trades, ETH L2 book, BTC/ETH orders...")
    print("-" * 60)

    # Handle Ctrl+C
    def signal_handler(sig, frame):
        print("\nStopping...")
        stream.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    stream.start()

    # Run for 20 seconds
    time.sleep(20)

    stream.stop()

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Trades received: {counts['trades']}")
    print(f"  L2 updates:      {counts['l2']}")
    print(f"  Order events:    {counts['orders']}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("gRPC Streaming Examples")
    print("=" * 60)
    print(f"Endpoint: {ENDPOINT[:50]}...")
    print()
    print("This demo shows all gRPC streaming capabilities:")
    print("  1. Trades — Real-time executed trades")
    print("  2. L2 Book — Aggregated order book by price level")
    print("  3. L4 Book — Individual orders (CRITICAL for trading)")
    print("  4. Orders — Order lifecycle events")
    print("  5. Blocks — Block data")
    print("  6. Multi-stream — Multiple subscriptions + management")
    print()

    # Run examples
    try:
        stream_trades_example()
        stream_l2_book_example()
        stream_l4_book_example()
        stream_orders_example()
        stream_blocks_example()
        # multi_stream_example()  # Uncomment for full demo

        print()
        print("=" * 60)
        print("All examples completed!")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\nDemo interrupted.")
    except Exception as e:
        print(f"\nError: {e}")
        raise
