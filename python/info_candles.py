#!/usr/bin/env python3
"""
Historical Candles Example

Shows how to fetch historical candlestick (OHLCV) data.

Note: candleSnapshot may not be available on all QuickNode endpoints.
Check the QuickNode docs for method availability.

Setup:
    pip install hyperliquid-sdk

Usage:
    export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
    python info_candles.py
"""

import os
import time
from hyperliquid_sdk import Info

ENDPOINT = os.environ.get("ENDPOINT")
if not ENDPOINT:
    print("Set ENDPOINT environment variable")
    exit(1)

info = Info(ENDPOINT)

print("=" * 50)
print("Historical Candles")
print("=" * 50)

# Last 24 hours
now = int(time.time() * 1000)
day_ago = now - (24 * 60 * 60 * 1000)

# Fetch BTC 1-hour candles
print("\n1. BTC 1-Hour Candles (last 24h):")
try:
    candles = info.candles("BTC", "1h", day_ago, now)
    print(f"   Retrieved {len(candles)} candles")
    if candles:
        for c in candles[-3:]:
            print(f"   O:{c.get('o')} H:{c.get('h')} L:{c.get('l')} C:{c.get('c')}")
except Exception as e:
    print(f"   Error: {e}")
    print("   Note: candleSnapshot may not be available on this endpoint")

# Funding history
print("\n2. BTC Funding History:")
try:
    funding = info.funding_history("BTC", day_ago, now)
    print(f"   {len(funding)} entries")
    for f in funding[-3:]:
        print(f"   Rate: {f.get('fundingRate')}")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 50)
print("Done!")
