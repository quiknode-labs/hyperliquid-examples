#!/usr/bin/env python3
"""
Order Book Streaming Example — L2 and L4 Order Books

This example demonstrates how to stream order book data:
- L2 Book: Aggregated by price level (WebSocket or gRPC)
- L4 Book: Individual orders with order IDs (gRPC only)

L4 order book is CRITICAL for:
- Market making: Know exact queue position and order sizes
- Order flow analysis: Detect large orders and icebergs
- Optimal execution: See exactly what you're crossing
- Latency-sensitive trading: Lower latency than WebSocket

Setup:
    pip install hyperliquid-sdk

Usage:
    export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
    python stream_orderbook.py
"""

import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Any

from hyperliquid_sdk import GRPCStream, Stream, ConnectionState

ENDPOINT = os.environ.get("ENDPOINT")
if not ENDPOINT:
    print("Order Book Streaming Example")
    print("=" * 60)
    print()
    print("Usage:")
    print("  export ENDPOINT='https://YOUR-ENDPOINT.quiknode.pro/TOKEN'")
    print("  python stream_orderbook.py")
    sys.exit(1)


def timestamp():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


# ═══════════════════════════════════════════════════════════════════════════════
# L2 ORDER BOOK (Aggregated Price Levels)
# ═══════════════════════════════════════════════════════════════════════════════

class L2BookTracker:
    """Track L2 order book state."""

    def __init__(self, coin: str):
        self.coin = coin
        self.bids: List[Dict[str, Any]] = []
        self.asks: List[Dict[str, Any]] = []
        self.last_update = 0.0

    def update(self, data: Dict[str, Any]) -> None:
        """Update book from L2 data."""
        self.bids = data.get("bids", [])
        self.asks = data.get("asks", [])
        self.last_update = time.time()

    def best_bid(self) -> tuple:
        """Return (price, size) of best bid."""
        if not self.bids:
            return (0.0, 0.0)
        bid = self.bids[0]
        if isinstance(bid, list):
            return (float(bid[0]), float(bid[1]))
        return (float(bid.get("px", 0)), float(bid.get("sz", 0)))

    def best_ask(self) -> tuple:
        """Return (price, size) of best ask."""
        if not self.asks:
            return (0.0, 0.0)
        ask = self.asks[0]
        if isinstance(ask, list):
            return (float(ask[0]), float(ask[1]))
        return (float(ask.get("px", 0)), float(ask.get("sz", 0)))

    def spread(self) -> float:
        """Return spread in price."""
        bid_px, _ = self.best_bid()
        ask_px, _ = self.best_ask()
        return ask_px - bid_px if bid_px and ask_px else 0.0

    def spread_bps(self) -> float:
        """Return spread in basis points."""
        bid_px, _ = self.best_bid()
        ask_px, _ = self.best_ask()
        if not bid_px or not ask_px:
            return 0.0
        mid = (bid_px + ask_px) / 2
        return (ask_px - bid_px) / mid * 10000

    def depth(self, levels: int = 5) -> Dict[str, float]:
        """Return total size at top N levels."""
        def sum_size(book: List) -> float:
            total = 0.0
            for level in book[:levels]:
                if isinstance(level, list) and len(level) >= 2:
                    total += float(level[1])
                elif isinstance(level, dict):
                    total += float(level.get("sz", 0))
            return total

        return {
            "bid_depth": sum_size(self.bids),
            "ask_depth": sum_size(self.asks),
        }

    def display(self) -> None:
        """Display current book state."""
        bid_px, bid_sz = self.best_bid()
        ask_px, ask_sz = self.best_ask()
        depth = self.depth()

        print(f"\n{self.coin} L2 Order Book")
        print("-" * 40)
        print(f"  Best Bid:   ${bid_px:>12,.2f} x {bid_sz:>10.4f}")
        print(f"  Best Ask:   ${ask_px:>12,.2f} x {ask_sz:>10.4f}")
        print(f"  Spread:     ${self.spread():>12,.2f} ({self.spread_bps():.2f} bps)")
        print(f"  Bid Depth:  {depth['bid_depth']:>23.4f} (top 5)")
        print(f"  Ask Depth:  {depth['ask_depth']:>23.4f} (top 5)")
        print(f"  Levels:     {len(self.bids)} bids, {len(self.asks)} asks")


def stream_l2_grpc():
    """Stream L2 order book via gRPC."""
    print("\n" + "=" * 60)
    print("L2 ORDER BOOK via gRPC")
    print("=" * 60)
    print()
    print("L2 book aggregates all orders at each price level.")
    print("n_sig_figs controls aggregation precision.")
    print()

    tracker = L2BookTracker("BTC")
    update_count = 0

    def on_l2(data: Dict[str, Any]):
        nonlocal update_count
        update_count += 1
        tracker.update(data)

        if update_count <= 3:
            tracker.display()

    stream = GRPCStream(ENDPOINT, reconnect=False)

    # n_sig_figs options:
    # - 5: Full precision (most levels)
    # - 4: Some aggregation
    # - 3: More aggregation (fewer levels, larger sizes)
    stream.l2_book("BTC", on_l2, n_sig_figs=5)

    print("Subscribing to BTC L2 book via gRPC...")
    print("-" * 60)

    stream.start()

    start = time.time()
    while update_count < 3 and time.time() - start < 15:
        time.sleep(0.1)

    stream.stop()
    print(f"\nReceived {update_count} L2 updates via gRPC")


def stream_l2_websocket():
    """Stream L2 order book via WebSocket."""
    print("\n" + "=" * 60)
    print("L2 ORDER BOOK via WebSocket")
    print("=" * 60)

    tracker = L2BookTracker("BTC")
    update_count = 0

    def on_l2(data: Dict[str, Any]):
        nonlocal update_count
        update_count += 1

        # WebSocket format: {"channel": "l2Book", "data": {...}}
        book = data.get("data", {})
        levels = book.get("levels", [[], []])

        # Convert to common format
        converted = {
            "bids": levels[0] if len(levels) > 0 else [],
            "asks": levels[1] if len(levels) > 1 else [],
        }
        tracker.update(converted)

        if update_count <= 3:
            tracker.display()

    stream = Stream(ENDPOINT, reconnect=False)
    stream.l2_book("BTC", on_l2)

    print("Subscribing to BTC L2 book via WebSocket...")
    print("-" * 60)

    stream.start()

    start = time.time()
    while update_count < 3 and time.time() - start < 15:
        time.sleep(0.1)

    stream.stop()
    print(f"\nReceived {update_count} L2 updates via WebSocket")


# ═══════════════════════════════════════════════════════════════════════════════
# L4 ORDER BOOK (Individual Orders) — CRITICAL FOR TRADING
# ═══════════════════════════════════════════════════════════════════════════════

class L4BookTracker:
    """Track L4 order book with individual orders."""

    def __init__(self, coin: str):
        self.coin = coin
        self.bids: Dict[str, Dict[str, Any]] = {}  # oid -> order
        self.asks: Dict[str, Dict[str, Any]] = {}  # oid -> order
        self.last_update = 0.0

    def update(self, data: Dict[str, Any]) -> None:
        """Update book from L4 data."""
        self.last_update = time.time()

        # Process bids
        for bid in data.get("bids", []):
            self._process_level(bid, self.bids, "bid")

        # Process asks
        for ask in data.get("asks", []):
            self._process_level(ask, self.asks, "ask")

    def _process_level(self, level: Any, book: Dict, side: str) -> None:
        """Process a single price level."""
        if isinstance(level, list):
            if len(level) >= 3:
                # Format: [price, size, order_id]
                px, sz, oid = level[0], level[1], str(level[2])
                if float(sz) == 0:
                    book.pop(oid, None)
                else:
                    book[oid] = {"px": px, "sz": sz, "oid": oid, "side": side}
            elif len(level) >= 2 and isinstance(level[1], list):
                # Format: [price, [[size, oid], ...]]
                px = level[0]
                for order in level[1]:
                    if isinstance(order, list) and len(order) >= 2:
                        sz, oid = order[0], str(order[1])
                        if float(sz) == 0:
                            book.pop(oid, None)
                        else:
                            book[oid] = {"px": px, "sz": sz, "oid": oid, "side": side}

    def get_sorted_bids(self) -> List[Dict]:
        """Return bids sorted by price (highest first)."""
        return sorted(
            self.bids.values(),
            key=lambda x: float(x["px"]),
            reverse=True
        )

    def get_sorted_asks(self) -> List[Dict]:
        """Return asks sorted by price (lowest first)."""
        return sorted(
            self.asks.values(),
            key=lambda x: float(x["px"])
        )

    def orders_at_price(self, price: float, side: str = "bid") -> List[Dict]:
        """Get all orders at a specific price."""
        book = self.bids if side == "bid" else self.asks
        return [
            order for order in book.values()
            if abs(float(order["px"]) - price) < 0.01  # Price tolerance
        ]

    def total_orders(self) -> tuple:
        """Return (bid_count, ask_count)."""
        return (len(self.bids), len(self.asks))

    def display(self, levels: int = 5) -> None:
        """Display current L4 book state."""
        sorted_bids = self.get_sorted_bids()
        sorted_asks = self.get_sorted_asks()

        print(f"\n{self.coin} L4 Order Book (Individual Orders)")
        print("=" * 60)

        # Group orders by price
        bid_prices: Dict[float, List[Dict]] = {}
        for bid in sorted_bids[:20]:  # Top 20 orders
            px = float(bid["px"])
            if px not in bid_prices:
                bid_prices[px] = []
            bid_prices[px].append(bid)

        ask_prices: Dict[float, List[Dict]] = {}
        for ask in sorted_asks[:20]:
            px = float(ask["px"])
            if px not in ask_prices:
                ask_prices[px] = []
            ask_prices[px].append(ask)

        # Display asks (top levels, reversed for display)
        print("\nASKS (top 5 price levels):")
        sorted_ask_prices = sorted(ask_prices.keys())[:levels]
        for px in reversed(sorted_ask_prices):
            orders = ask_prices[px]
            total_sz = sum(float(o["sz"]) for o in orders)
            print(f"  ${px:>12,.2f} | {total_sz:>10.4f} | {len(orders):>3} orders")
            # Show individual orders (first 3)
            for i, order in enumerate(orders[:3]):
                print(f"               └─ {float(order['sz']):>10.4f} (oid: {order['oid'][:8]}...)")

        print("  " + "-" * 56)
        print("  " + " " * 14 + "SPREAD")
        print("  " + "-" * 56)

        # Display bids (top levels)
        print("\nBIDS (top 5 price levels):")
        sorted_bid_prices = sorted(bid_prices.keys(), reverse=True)[:levels]
        for px in sorted_bid_prices:
            orders = bid_prices[px]
            total_sz = sum(float(o["sz"]) for o in orders)
            print(f"  ${px:>12,.2f} | {total_sz:>10.4f} | {len(orders):>3} orders")
            for i, order in enumerate(orders[:3]):
                print(f"               └─ {float(order['sz']):>10.4f} (oid: {order['oid'][:8]}...)")

        bid_count, ask_count = self.total_orders()
        print(f"\nTotal: {bid_count} bid orders, {ask_count} ask orders")


def stream_l4_book():
    """Stream L4 order book via gRPC (individual orders)."""
    print("\n" + "=" * 60)
    print("L4 ORDER BOOK via gRPC (Individual Orders)")
    print("=" * 60)
    print()
    print("L4 book shows EVERY individual order with order ID.")
    print("This is CRITICAL for market making and order flow analysis.")
    print()
    print("Use cases:")
    print("  - See exact queue position")
    print("  - Detect large orders / icebergs")
    print("  - Know exactly what you're crossing")
    print("  - Analyze order flow")
    print()

    tracker = L4BookTracker("BTC")
    update_count = 0

    def on_l4(data: Dict[str, Any]):
        nonlocal update_count
        update_count += 1
        tracker.update(data)

        if update_count <= 3:
            tracker.display(levels=3)
            print()

    stream = GRPCStream(ENDPOINT, reconnect=False)
    stream.l4_book("BTC", on_l4)

    print("Subscribing to BTC L4 book via gRPC...")
    print("-" * 60)

    stream.start()

    start = time.time()
    while update_count < 3 and time.time() - start < 15:
        time.sleep(0.1)

    stream.stop()
    print(f"\nReceived {update_count} L4 updates")


# ═══════════════════════════════════════════════════════════════════════════════
# COMPARISON: L2 vs L4 Order Book
# ═══════════════════════════════════════════════════════════════════════════════

def comparison():
    """Show comparison between L2 and L4 order books."""
    print("\n" + "=" * 60)
    print("L2 vs L4 ORDER BOOK COMPARISON")
    print("=" * 60)
    print()
    print("┌─────────────────────────────────────────────────────────────┐")
    print("│                    L2 ORDER BOOK                            │")
    print("├─────────────────────────────────────────────────────────────┤")
    print("│ • Aggregated by price level                                 │")
    print("│ • Shows total size at each price                            │")
    print("│ • Available via WebSocket AND gRPC                          │")
    print("│ • Lower bandwidth                                           │")
    print("│ • Good for: Price monitoring, simple trading                │")
    print("├─────────────────────────────────────────────────────────────┤")
    print("│ Example:                                                    │")
    print("│   Price: $95,000.00 | Total Size: 10.5 BTC                  │")
    print("│   (You don't know how many orders or their sizes)           │")
    print("└─────────────────────────────────────────────────────────────┘")
    print()
    print("┌─────────────────────────────────────────────────────────────┐")
    print("│                    L4 ORDER BOOK                            │")
    print("├─────────────────────────────────────────────────────────────┤")
    print("│ • Individual orders with order IDs                          │")
    print("│ • Shows each order separately                               │")
    print("│ • Available via gRPC ONLY (higher performance)              │")
    print("│ • Higher bandwidth but more detail                          │")
    print("│ • Good for: Market making, HFT, order flow analysis         │")
    print("├─────────────────────────────────────────────────────────────┤")
    print("│ Example:                                                    │")
    print("│   Price: $95,000.00                                         │")
    print("│     └─ Order 1: 5.0 BTC (oid: abc123...)                    │")
    print("│     └─ Order 2: 3.0 BTC (oid: def456...)                    │")
    print("│     └─ Order 3: 2.5 BTC (oid: ghi789...)                    │")
    print("│   (You see every order and can track queue position)        │")
    print("└─────────────────────────────────────────────────────────────┘")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("Order Book Streaming Examples")
    print("=" * 60)
    print(f"Endpoint: {ENDPOINT[:50]}...")

    try:
        # Show comparison
        comparison()

        # Run L2 examples
        stream_l2_grpc()
        stream_l2_websocket()

        # Run L4 example (CRITICAL)
        stream_l4_book()

        print()
        print("=" * 60)
        print("All examples completed!")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\nDemo interrupted.")
    except Exception as e:
        print(f"\nError: {e}")
        raise
