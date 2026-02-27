#!/usr/bin/env python3
"""
L4 Order Book Streaming via gRPC — Individual Orders with Order IDs

L4 order book is CRITICAL for:
- Market making: Know your exact queue position
- Order flow analysis: Detect large orders, icebergs
- Optimal execution: See exactly what you're crossing
- HFT: Lower latency than WebSocket

This example shows how to:
1. Stream L4 order book updates
2. Track individual orders
3. Calculate depth and queue position

Setup:
    pip install hyperliquid-sdk

Usage:
    export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
    python stream_l4_book.py
"""

import os
import signal
import sys
import time
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict

from hyperliquid_sdk import GRPCStream, ConnectionState

ENDPOINT = os.environ.get("ENDPOINT")
if not ENDPOINT:
    print("L4 Order Book Streaming Example")
    print("=" * 60)
    print()
    print("L4 book shows EVERY individual order with order IDs.")
    print("This is essential for market making and order flow analysis.")
    print()
    print("Usage:")
    print("  export ENDPOINT='https://YOUR-ENDPOINT.quiknode.pro/TOKEN'")
    print("  python stream_l4_book.py")
    sys.exit(1)


def timestamp():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


class L4BookManager:
    """
    Manage L4 order book state.

    L4 book tracks individual orders with their order IDs,
    allowing you to:
    - Know exact queue position at each price level
    - Track specific orders (your own or large orders)
    - Calculate precise depth
    """

    def __init__(self, coin: str):
        self.coin = coin
        # Store orders by order ID
        self.bids: Dict[str, Dict[str, Any]] = {}
        self.asks: Dict[str, Dict[str, Any]] = {}
        self.update_count = 0
        self.last_update = 0.0

    def process_update(self, data: Dict[str, Any]) -> None:
        """Process L4 book update."""
        self.update_count += 1
        self.last_update = time.time()

        # Process bids
        for level in data.get("bids", []):
            self._process_level(level, self.bids, "bid")

        # Process asks
        for level in data.get("asks", []):
            self._process_level(level, self.asks, "ask")

    def _process_level(self, level: Any, book: Dict, side: str) -> None:
        """Process a single order level."""
        if not isinstance(level, list):
            return

        # Format 1: [price, size, order_id]
        if len(level) >= 3 and not isinstance(level[1], list):
            px, sz, oid = str(level[0]), str(level[1]), str(level[2])
            if float(sz) == 0:
                # Order removed
                book.pop(oid, None)
            else:
                # Order added or updated
                book[oid] = {
                    "px": px,
                    "sz": sz,
                    "oid": oid,
                    "side": side,
                    "time": time.time(),
                }

        # Format 2: [price, [[size, oid], ...]]
        elif len(level) >= 2 and isinstance(level[1], list):
            px = str(level[0])
            for order in level[1]:
                if isinstance(order, list) and len(order) >= 2:
                    sz, oid = str(order[0]), str(order[1])
                    if float(sz) == 0:
                        book.pop(oid, None)
                    else:
                        book[oid] = {
                            "px": px,
                            "sz": sz,
                            "oid": oid,
                            "side": side,
                            "time": time.time(),
                        }

    def get_sorted_bids(self) -> List[Dict]:
        """Get bids sorted by price (highest first)."""
        return sorted(
            self.bids.values(),
            key=lambda x: float(x["px"]),
            reverse=True,
        )

    def get_sorted_asks(self) -> List[Dict]:
        """Get asks sorted by price (lowest first)."""
        return sorted(
            self.asks.values(),
            key=lambda x: float(x["px"]),
        )

    def get_best_bid(self) -> Dict[str, Any]:
        """Get best bid order."""
        sorted_bids = self.get_sorted_bids()
        return sorted_bids[0] if sorted_bids else {}

    def get_best_ask(self) -> Dict[str, Any]:
        """Get best ask order."""
        sorted_asks = self.get_sorted_asks()
        return sorted_asks[0] if sorted_asks else {}

    def get_spread(self) -> float:
        """Get current spread."""
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()
        if best_bid and best_ask:
            return float(best_ask["px"]) - float(best_bid["px"])
        return 0.0

    def get_orders_at_price(self, price: float, side: str = "bid") -> List[Dict]:
        """Get all orders at a specific price level."""
        book = self.bids if side == "bid" else self.asks
        return [
            order for order in book.values()
            if abs(float(order["px"]) - price) < 0.01
        ]

    def get_queue_position(self, order_id: str) -> int:
        """
        Get queue position for an order.

        Returns position (1 = first in queue) or 0 if not found.
        """
        # Check bids
        for order in self.bids.values():
            if order["oid"] == order_id:
                price = float(order["px"])
                orders_at_price = self.get_orders_at_price(price, "bid")
                # Sort by time (earlier = better position)
                sorted_orders = sorted(orders_at_price, key=lambda x: x.get("time", 0))
                for i, o in enumerate(sorted_orders):
                    if o["oid"] == order_id:
                        return i + 1
                return 0

        # Check asks
        for order in self.asks.values():
            if order["oid"] == order_id:
                price = float(order["px"])
                orders_at_price = self.get_orders_at_price(price, "ask")
                sorted_orders = sorted(orders_at_price, key=lambda x: x.get("time", 0))
                for i, o in enumerate(sorted_orders):
                    if o["oid"] == order_id:
                        return i + 1
                return 0

        return 0

    def get_depth_at_levels(self, levels: int = 5) -> Dict[str, Any]:
        """Get depth at top N price levels."""
        sorted_bids = self.get_sorted_bids()
        sorted_asks = self.get_sorted_asks()

        # Group by price
        bid_by_price: Dict[float, float] = defaultdict(float)
        for order in sorted_bids:
            bid_by_price[float(order["px"])] += float(order["sz"])

        ask_by_price: Dict[float, float] = defaultdict(float)
        for order in sorted_asks:
            ask_by_price[float(order["px"])] += float(order["sz"])

        # Get top N levels
        bid_prices = sorted(bid_by_price.keys(), reverse=True)[:levels]
        ask_prices = sorted(ask_by_price.keys())[:levels]

        bid_depth = sum(bid_by_price[p] for p in bid_prices)
        ask_depth = sum(ask_by_price[p] for p in ask_prices)

        return {
            "bid_depth": bid_depth,
            "ask_depth": ask_depth,
            "bid_levels": len(bid_prices),
            "ask_levels": len(ask_prices),
            "bid_orders": len(self.bids),
            "ask_orders": len(self.asks),
        }

    def display(self, levels: int = 3) -> None:
        """Display current L4 book state."""
        sorted_bids = self.get_sorted_bids()
        sorted_asks = self.get_sorted_asks()
        depth = self.get_depth_at_levels(levels)

        print(f"\n{'=' * 60}")
        print(f"{self.coin} L4 ORDER BOOK (Update #{self.update_count})")
        print(f"{'=' * 60}")

        # Group orders by price for display
        ask_by_price: Dict[float, List[Dict]] = defaultdict(list)
        for order in sorted_asks[:20]:
            ask_by_price[float(order["px"])].append(order)

        bid_by_price: Dict[float, List[Dict]] = defaultdict(list)
        for order in sorted_bids[:20]:
            bid_by_price[float(order["px"])].append(order)

        # Display asks (reversed so best ask is near spread)
        print("\n ASKS:")
        ask_prices = sorted(ask_by_price.keys())[:levels]
        for px in reversed(ask_prices):
            orders = ask_by_price[px]
            total_sz = sum(float(o["sz"]) for o in orders)
            print(f"  ${px:>12,.2f} │ {total_sz:>10.4f} │ {len(orders):>2} orders")
            # Show first 2 orders at this level
            for order in orders[:2]:
                print(f"               │ └─ {float(order['sz']):>10.4f} (oid: {order['oid'][:12]}...)")

        # Spread
        spread = self.get_spread()
        print(f"\n  {'─' * 44}")
        print(f"  SPREAD: ${spread:,.2f}")
        print(f"  {'─' * 44}\n")

        # Display bids
        print(" BIDS:")
        bid_prices = sorted(bid_by_price.keys(), reverse=True)[:levels]
        for px in bid_prices:
            orders = bid_by_price[px]
            total_sz = sum(float(o["sz"]) for o in orders)
            print(f"  ${px:>12,.2f} │ {total_sz:>10.4f} │ {len(orders):>2} orders")
            for order in orders[:2]:
                print(f"               │ └─ {float(order['sz']):>10.4f} (oid: {order['oid'][:12]}...)")

        # Summary
        print(f"\n SUMMARY:")
        print(f"  Total Bid Orders: {depth['bid_orders']:>6}")
        print(f"  Total Ask Orders: {depth['ask_orders']:>6}")
        print(f"  Bid Depth (top {levels}): {depth['bid_depth']:>10.4f}")
        print(f"  Ask Depth (top {levels}): {depth['ask_depth']:>10.4f}")


def main():
    print("=" * 60)
    print("L4 ORDER BOOK STREAMING (gRPC)")
    print("=" * 60)
    print(f"Endpoint: {ENDPOINT[:50]}...")
    print()
    print("L4 book shows individual orders with order IDs.")
    print("This is essential for:")
    print("  - Market making (queue position)")
    print("  - Order flow analysis (large orders)")
    print("  - Optimal execution (what you're crossing)")
    print()

    # Create book manager
    book = L4BookManager("BTC")

    def on_l4_update(data: Dict[str, Any]):
        """Handle L4 book update."""
        book.process_update(data)

        # Display every update for first 5, then every 10th
        if book.update_count <= 5 or book.update_count % 10 == 0:
            book.display(levels=3)

        if book.update_count >= 30:
            print(f"\nReceived {book.update_count} updates. Stopping...")

    def on_state(state: ConnectionState):
        print(f"[{timestamp()}] Connection state: {state.value}")

    def on_error(error):
        print(f"[{timestamp()}] Error: {error}")

    def on_connect():
        print(f"[{timestamp()}] Connected to L4 book stream")

    # Create gRPC stream
    stream = GRPCStream(
        ENDPOINT,
        on_error=on_error,
        on_connect=on_connect,
        on_state_change=on_state,
        reconnect=True,
    )

    # Subscribe to L4 book
    print("Subscribing to BTC L4 order book...")
    stream.l4_book("BTC", on_l4_update)

    # Handle Ctrl+C
    def signal_handler(sig, frame):
        print("\n\nStopping...")
        stream.stop()
        print(f"\nFinal stats:")
        print(f"  Total updates: {book.update_count}")
        print(f"  Total bid orders: {len(book.bids)}")
        print(f"  Total ask orders: {len(book.asks)}")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    print("-" * 60)
    print("Streaming L4 book... (Ctrl+C to stop)")
    print()

    # Start streaming
    stream.start()

    # Run for 60 seconds or until we have 30 updates
    start = time.time()
    while book.update_count < 30 and time.time() - start < 60:
        time.sleep(0.5)

    stream.stop()

    print()
    print("=" * 60)
    print("L4 BOOK STREAMING COMPLETE")
    print("=" * 60)
    print(f"Total updates received: {book.update_count}")
    print(f"Final bid orders: {len(book.bids)}")
    print(f"Final ask orders: {len(book.asks)}")


if __name__ == "__main__":
    main()
