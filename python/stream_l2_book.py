#!/usr/bin/env python3
"""
L2 Order Book Streaming — Aggregated Price Levels

L2 order book shows total size at each price level (aggregated).
Available via both WebSocket and gRPC.

Use L2 for:
- Price monitoring
- Basic trading strategies
- Lower bandwidth requirements

Use L4 (gRPC only) when you need:
- Individual order IDs
- Queue position tracking
- Order flow analysis

Setup:
    pip install hyperliquid-sdk

Usage:
    export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
    python stream_l2_book.py
"""

import os
import signal
import sys
import time
from datetime import datetime
from typing import Dict, List, Any

from hyperliquid_sdk import GRPCStream, Stream, ConnectionState

ENDPOINT = os.environ.get("ENDPOINT")
if not ENDPOINT:
    print("L2 Order Book Streaming Example")
    print("=" * 60)
    print()
    print("Usage:")
    print("  export ENDPOINT='https://YOUR-ENDPOINT.quiknode.pro/TOKEN'")
    print("  python stream_l2_book.py")
    sys.exit(1)


def timestamp():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


class L2BookTracker:
    """Track L2 order book state."""

    def __init__(self, coin: str, source: str = "grpc"):
        self.coin = coin
        self.source = source
        self.bids: List[Any] = []
        self.asks: List[Any] = []
        self.update_count = 0

    def update_from_grpc(self, data: Dict[str, Any]) -> None:
        """Update from gRPC format."""
        self.update_count += 1
        self.bids = data.get("bids", [])
        self.asks = data.get("asks", [])

    def update_from_websocket(self, data: Dict[str, Any]) -> None:
        """Update from WebSocket format."""
        self.update_count += 1
        book = data.get("data", {})
        levels = book.get("levels", [[], []])
        self.bids = levels[0] if len(levels) > 0 else []
        self.asks = levels[1] if len(levels) > 1 else []

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
        bid_px, _ = self.best_bid()
        ask_px, _ = self.best_ask()
        return ask_px - bid_px if bid_px and ask_px else 0.0

    def spread_bps(self) -> float:
        bid_px, _ = self.best_bid()
        ask_px, _ = self.best_ask()
        if not bid_px or not ask_px:
            return 0.0
        mid = (bid_px + ask_px) / 2
        return (ask_px - bid_px) / mid * 10000

    def display(self, levels: int = 5) -> None:
        """Display L2 book."""
        bid_px, bid_sz = self.best_bid()
        ask_px, ask_sz = self.best_ask()

        print(f"\n[{timestamp()}] {self.coin} L2 Book ({self.source.upper()}) #{self.update_count}")
        print("-" * 50)

        # Show top ask levels (reversed)
        print(" ASKS:")
        for i, ask in enumerate(reversed(self.asks[:levels])):
            if isinstance(ask, list):
                px, sz = float(ask[0]), float(ask[1])
            else:
                px, sz = float(ask.get("px", 0)), float(ask.get("sz", 0))
            print(f"    ${px:>12,.2f} │ {sz:>10.4f}")

        print(f"  {'─' * 30}")
        print(f"  SPREAD: ${self.spread():,.2f} ({self.spread_bps():.1f} bps)")
        print(f"  {'─' * 30}")

        # Show top bid levels
        print(" BIDS:")
        for i, bid in enumerate(self.bids[:levels]):
            if isinstance(bid, list):
                px, sz = float(bid[0]), float(bid[1])
            else:
                px, sz = float(bid.get("px", 0)), float(bid.get("sz", 0))
            print(f"    ${px:>12,.2f} │ {sz:>10.4f}")

        print(f"\n  Levels: {len(self.bids)} bids, {len(self.asks)} asks")


# ═══════════════════════════════════════════════════════════════════════════════
# gRPC L2 BOOK
# ═══════════════════════════════════════════════════════════════════════════════

def stream_l2_grpc():
    """Stream L2 book via gRPC."""
    print("\n" + "=" * 60)
    print("L2 ORDER BOOK via gRPC")
    print("=" * 60)
    print()
    print("gRPC provides lower latency than WebSocket.")
    print("n_sig_figs controls price aggregation (3-5).")
    print()

    book = L2BookTracker("BTC", source="grpc")

    def on_l2(data: Dict[str, Any]):
        book.update_from_grpc(data)
        if book.update_count <= 5:
            book.display(levels=3)

    def on_connect():
        print(f"[{timestamp()}] gRPC connected")

    stream = GRPCStream(ENDPOINT, on_connect=on_connect, reconnect=False)

    # n_sig_figs options:
    # 5 = full precision (most levels)
    # 4 = some aggregation
    # 3 = more aggregation (fewer levels, larger sizes)
    stream.l2_book("BTC", on_l2, n_sig_figs=5)

    print("Subscribing to BTC L2 book via gRPC (n_sig_figs=5)...")
    print("-" * 60)

    stream.start()

    start = time.time()
    while book.update_count < 5 and time.time() - start < 15:
        time.sleep(0.1)

    stream.stop()
    print(f"\nReceived {book.update_count} L2 updates via gRPC")


# ═══════════════════════════════════════════════════════════════════════════════
# WebSocket L2 BOOK
# ═══════════════════════════════════════════════════════════════════════════════

def stream_l2_websocket():
    """Stream L2 book via WebSocket."""
    print("\n" + "=" * 60)
    print("L2 ORDER BOOK via WebSocket")
    print("=" * 60)

    book = L2BookTracker("BTC", source="websocket")

    def on_l2(data: Dict[str, Any]):
        book.update_from_websocket(data)
        if book.update_count <= 5:
            book.display(levels=3)

    def on_open():
        print(f"[{timestamp()}] WebSocket connected")

    stream = Stream(ENDPOINT, on_open=on_open, reconnect=False)
    stream.l2_book("BTC", on_l2)

    print("Subscribing to BTC L2 book via WebSocket...")
    print("-" * 60)

    stream.start()

    start = time.time()
    while book.update_count < 5 and time.time() - start < 15:
        time.sleep(0.1)

    stream.stop()
    print(f"\nReceived {book.update_count} L2 updates via WebSocket")


# ═══════════════════════════════════════════════════════════════════════════════
# COMPARE L2 SOURCES
# ═══════════════════════════════════════════════════════════════════════════════

def compare_sources():
    """Compare L2 book from both sources."""
    print("\n" + "=" * 60)
    print("COMPARISON: gRPC vs WebSocket")
    print("=" * 60)
    print()
    print("┌─────────────────────────────────────────────────────────────┐")
    print("│                      L2 VIA gRPC                            │")
    print("├─────────────────────────────────────────────────────────────┤")
    print("│ • Lower latency                                             │")
    print("│ • n_sig_figs parameter for aggregation control              │")
    print("│ • Best for: HFT, latency-sensitive apps                     │")
    print("│ • Port: 10000                                               │")
    print("└─────────────────────────────────────────────────────────────┘")
    print()
    print("┌─────────────────────────────────────────────────────────────┐")
    print("│                    L2 VIA WebSocket                         │")
    print("├─────────────────────────────────────────────────────────────┤")
    print("│ • Standard WebSocket (443)                                  │")
    print("│ • Works in browsers                                         │")
    print("│ • More subscription types available                         │")
    print("│ • Best for: Web apps, general use                           │")
    print("└─────────────────────────────────────────────────────────────┘")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("L2 ORDER BOOK STREAMING")
    print("=" * 60)
    print(f"Endpoint: {ENDPOINT[:50]}...")

    try:
        # Show comparison
        compare_sources()

        # Stream via gRPC
        stream_l2_grpc()

        # Stream via WebSocket
        stream_l2_websocket()

        print()
        print("=" * 60)
        print("All L2 examples completed!")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\nDemo interrupted.")
    except Exception as e:
        print(f"\nError: {e}")
        raise
