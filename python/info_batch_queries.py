#!/usr/bin/env python3
"""
Multi-User Queries Example

Shows how to query multiple users' states efficiently.

Setup:
    pip install hyperliquid-sdk

Usage:
    export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
    python info_batch_queries.py
"""

import os
from hyperliquid_sdk import HyperliquidSDK

ENDPOINT = os.environ.get("ENDPOINT")
if not ENDPOINT:
    print("Set ENDPOINT environment variable")
    exit(1)

# Single SDK instance — access everything through sdk.info, sdk.core, sdk.evm, etc.
sdk = HyperliquidSDK(ENDPOINT)
info = sdk.info

print("=" * 50)
print("Multi-User Queries")
print("=" * 50)

# Example addresses (use real addresses with activity for better demo)
addresses = [
    "0x2ba553d9f990a3b66b03b2dc0d030dfc1c061036",  # Active trader
    "0x0000000000000000000000000000000000000001",
    "0x0000000000000000000000000000000000000002",
]

print(f"\nQuerying {len(addresses)} user accounts...")

# Query each user's clearinghouse state
print("\n1. User Account States:")
for addr in addresses:
    try:
        state = info.clearinghouse_state(addr)
        margin = state.get("marginSummary", {})
        value = float(margin.get("accountValue", 0))
        positions = len(state.get("assetPositions", []))
        print(f"   {addr[:12]}...: ${value:,.2f} ({positions} positions)")
    except Exception as e:
        print(f"   {addr[:12]}...: Error - {e}")

# Query open orders for first user
print("\n2. Open Orders (first user):")
try:
    orders = info.open_orders(addresses[0])
    print(f"   {len(orders)} open orders")
    for o in orders[:3]:
        side = "BUY" if o.get("side") == "B" else "SELL"
        print(f"   - {o.get('coin')}: {side} {o.get('sz')} @ {o.get('limitPx')}")
except Exception as e:
    print(f"   Error: {e}")

# Query user fees
print("\n3. Fee Structure (first user):")
try:
    fees = info.user_fees(addresses[0])
    print(f"   Maker: {fees.get('makerRate', 'N/A')}")
    print(f"   Taker: {fees.get('takerRate', 'N/A')}")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 50)
print("Done!")
