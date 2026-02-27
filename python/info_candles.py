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
from hyperliquid_sdk import HyperliquidSDK

ENDPOINT = os.environ.get("ENDPOINT")
if not ENDPOINT:
    print("Set ENDPOINT environment variable")
    exit(1)

# Single SDK instance — access everything through sdk.info, sdk.core, sdk.evm, etc.
sdk = HyperliquidSDK(ENDPOINT)
info = sdk.info

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

# Predicted funding rates (supported on QuickNode)
print("\n2. Predicted Funding Rates:")
try:
    fundings = info.predicted_fundings()
    print(f"   {len(fundings)} assets with funding rates:")
    # Structure: [[coin, [[source, {fundingRate, ...}], ...]], ...]
    for item in fundings[:5]:
        if isinstance(item, list) and len(item) >= 2:
            coin = item[0]
            sources = item[1]
            if sources and isinstance(sources, list) and len(sources) > 0:
                # Get HlPerp funding rate if available
                for src in sources:
                    if isinstance(src, list) and len(src) >= 2 and src[0] == "HlPerp":
                        rate = float(src[1].get("fundingRate", 0)) * 100
                        print(f"   {coin}: {rate:.4f}%")
                        break
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 50)
print("Done!")
