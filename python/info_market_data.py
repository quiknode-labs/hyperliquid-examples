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
from hyperliquid_sdk import HyperliquidSDK, HyperliquidError

ENDPOINT = os.environ.get("ENDPOINT")
if not ENDPOINT:
    print("Set ENDPOINT environment variable")
    print("Example: export ENDPOINT='https://your-endpoint.hype-mainnet.quiknode.pro/TOKEN'")
    exit(1)

# Single SDK instance — access everything through sdk.info, sdk.core, sdk.evm, etc.
sdk = HyperliquidSDK(ENDPOINT)
info = sdk.info

print("=" * 50)
print("Market Data (Info API)")
print("=" * 50)

# Exchange metadata
print("\n1. Exchange Metadata:")
try:
    meta = info.meta()
    print(f"   Perp Markets: {len(meta.get('universe', []))}")
    for asset in meta.get("universe", [])[:5]:
        print(f"   - {asset['name']}: max leverage {asset['maxLeverage']}x")
except HyperliquidError as e:
    print(f"   (meta not available: {e.code})")

# Spot metadata
print("\n2. Spot Metadata:")
try:
    spot = info.spot_meta()
    print(f"   Spot Tokens: {len(spot.get('tokens', []))}")
except HyperliquidError as e:
    print(f"   (spot_meta not available: {e.code})")

# Exchange status
print("\n3. Exchange Status:")
try:
    status = info.exchange_status()
    print(f"   {status}")
except HyperliquidError as e:
    print(f"   (exchange_status not available: {e.code})")

# All mid prices
print("\n4. Mid Prices:")
try:
    mids = info.all_mids()
    print(f"   BTC: ${float(mids.get('BTC', 0)):,.2f}")
    print(f"   ETH: ${float(mids.get('ETH', 0)):,.2f}")
except HyperliquidError as e:
    print(f"   (allMids not available: {e.code})")

# Order book
print("\n5. Order Book (BTC):")
try:
    book = info.l2_book("BTC")
    levels = book.get("levels", [[], []])
    if levels[0] and levels[1]:
        best_bid = float(levels[0][0].get("px", 0))
        best_ask = float(levels[1][0].get("px", 0))
        spread = best_ask - best_bid
        print(f"   Best Bid: ${best_bid:,.2f}")
        print(f"   Best Ask: ${best_ask:,.2f}")
        print(f"   Spread: ${spread:.2f}")
except HyperliquidError as e:
    print(f"   (l2_book not available: {e.code})")

# Recent trades
print("\n6. Recent Trades (BTC):")
try:
    trades = info.recent_trades("BTC")
    for t in trades[:3]:
        side = "BUY" if t.get("side") == "B" else "SELL"
        print(f"   {side} {t.get('sz')} @ ${float(t.get('px', 0)):,.2f}")
except HyperliquidError as e:
    print(f"   (recent_trades not available: {e.code})")

print("\n" + "=" * 50)
print("Done!")
