#!/usr/bin/env python3
"""
Batch Queries Example

Shows how to efficiently query multiple users' states in a single call.

Setup:
    pip install hyperliquid-sdk

Usage:
    export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
    python info_batch_queries.py
"""

import os
from hyperliquid_sdk import Info

ENDPOINT = os.environ.get("ENDPOINT")
if not ENDPOINT:
    print("Set ENDPOINT environment variable")
    exit(1)

info = Info(ENDPOINT)

print("=" * 50)
print("Batch Queries")
print("=" * 50)

# Example addresses
addresses = [
    "0x0000000000000000000000000000000000000001",
    "0x0000000000000000000000000000000000000002",
    "0x0000000000000000000000000000000000000003",
]

print(f"\nQuerying {len(addresses)} addresses in one call...")

# Batch clearinghouse states
print("\n1. Batch Clearinghouse States:")
states = info.batch_clearinghouse_states(addresses)
print(f"   Retrieved {len(states)} states")

for i, state in enumerate(states):
    margin = state.get("marginSummary", {})
    value = margin.get("accountValue", "0")
    print(f"   {addresses[i][:12]}...: ${value}")

print("\n2. Why Use Batch?")
print("   - 1 API call vs N individual calls")
print("   - Perfect for leaderboards, dashboards")

print("\n" + "=" * 50)
print("Done!")
