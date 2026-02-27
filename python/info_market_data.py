#!/usr/bin/env python3
"""
Market Data Example

Shows how to query market metadata, prices, order book, and recent trades.

The SDK handles all Info API methods automatically.

Setup:
    pip install hyperliquid-sdk

Usage:
    export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
    python info_market_data.py
"""

import os
from hyperliquid_sdk import Info

ENDPOINT = os.environ.get("ENDPOINT")
if not ENDPOINT:
    print("Set ENDPOINT environment variable")
    print("Example: export ENDPOINT='https://your-endpoint.hype-mainnet.quiknode.pro/TOKEN'")
    exit(1)

info = Info(ENDPOINT)

print("=" * 50)
print("Market Data (Info API)")
print("=" * 50)

# Exchange metadata
print("\n1. Exchange Metadata:")
meta = info.meta()
print(f"   Perp Markets: {len(meta.get('universe', []))}")
for asset in meta.get("universe", [])[:5]:
    print(f"   - {asset['name']}: max leverage {asset['maxLeverage']}x")

# Spot metadata
print("\n2. Spot Metadata:")
spot = info.spot_meta()
print(f"   Spot Tokens: {len(spot.get('tokens', []))}")

# Exchange status
print("\n3. Exchange Status:")
status = info.exchange_status()
print(f"   {status}")

# All mid prices
print("\n4. Mid Prices:")
mids = info.all_mids()
print(f"   BTC: ${float(mids.get('BTC', 0)):,.2f}")
print(f"   ETH: ${float(mids.get('ETH', 0)):,.2f}")

# Order book
print("\n5. Order Book (BTC):")
book = info.l2_book("BTC")
levels = book.get("levels", [[], []])
if levels[0] and levels[1]:
    best_bid = float(levels[0][0].get("px", 0))
    best_ask = float(levels[1][0].get("px", 0))
    spread = best_ask - best_bid
    print(f"   Best Bid: ${best_bid:,.2f}")
    print(f"   Best Ask: ${best_ask:,.2f}")
    print(f"   Spread: ${spread:.2f}")

# Recent trades
print("\n6. Recent Trades (BTC):")
trades = info.recent_trades("BTC")
for t in trades[:3]:
    side = "BUY" if t.get("side") == "B" else "SELL"
    print(f"   {side} {t.get('sz')} @ ${float(t.get('px', 0)):,.2f}")

print("\n" + "=" * 50)
print("Done!")
