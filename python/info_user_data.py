#!/usr/bin/env python3
"""
User Account Data Example

Shows how to query user positions, orders, and account state.

Setup:
    pip install hyperliquid-sdk

Usage:
    export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
    export USER_ADDRESS="0x..."
    python info_user_data.py
"""

import os
from hyperliquid_sdk import HyperliquidSDK, HyperliquidError

ENDPOINT = os.environ.get("ENDPOINT")
USER = os.environ.get("USER_ADDRESS", "0x2ba553d9f990a3b66b03b2dc0d030dfc1c061036")

if not ENDPOINT:
    print("Set ENDPOINT environment variable")
    exit(1)

# Single SDK instance — access everything through sdk.info, sdk.core, sdk.evm, etc.
sdk = HyperliquidSDK(ENDPOINT)
info = sdk.info

print("=" * 50)
print(f"User Data: {USER[:10]}...")
print("=" * 50)

# Clearinghouse state (positions + margin)
print("\n1. Positions & Margin:")
try:
    state = info.clearinghouse_state(USER)
    margin = state.get("marginSummary", {})
    print(f"   Account Value: ${margin.get('accountValue', '0')}")
    print(f"   Margin Used: ${margin.get('totalMarginUsed', '0')}")

    positions = state.get("assetPositions", [])
    if positions:
        print(f"   Positions: {len(positions)}")
        for pos in positions[:3]:
            p = pos.get("position", {})
            print(f"   - {p.get('coin')}: {p.get('szi')} @ {p.get('entryPx')}")
    else:
        print("   No positions")
except HyperliquidError as e:
    print(f"   (clearinghouse_state not available: {e.code})")

# Open orders
print("\n2. Open Orders:")
try:
    orders = info.open_orders(USER)
    if orders:
        print(f"   {len(orders)} orders:")
        for o in orders[:3]:
            side = "BUY" if o.get("side") == "B" else "SELL"
            print(f"   - {o.get('coin')}: {side} {o.get('sz')} @ {o.get('limitPx')}")
    else:
        print("   No open orders")
except HyperliquidError as e:
    print(f"   (open_orders not available: {e.code})")

# User fees
print("\n3. Fee Structure:")
try:
    fees = info.user_fees(USER)
    print(f"   Maker: {fees.get('makerRate', 'N/A')}")
    print(f"   Taker: {fees.get('takerRate', 'N/A')}")
except HyperliquidError as e:
    print(f"   (user_fees not available: {e.code})")

# Spot balances
print("\n4. Spot Balances:")
try:
    spot = info.spot_clearinghouse_state(USER)
    balances = spot.get("balances", [])
    if balances:
        for b in balances[:5]:
            print(f"   - {b.get('coin')}: {b.get('total')}")
    else:
        print("   No spot balances")
except HyperliquidError as e:
    print(f"   (spot_clearinghouse_state not available: {e.code})")

print("\n" + "=" * 50)
print("Done!")
