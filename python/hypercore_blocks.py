#!/usr/bin/env python3
"""
HyperCore Block Data Example

Shows how to get real-time trades, orders, and block data via the HyperCore API.

This is the alternative to Info methods (allMids, l2Book, recentTrades) that
are not available on QuickNode endpoints.

Setup:
    pip install hyperliquid-sdk

Usage:
    export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
    python hypercore_blocks.py
"""

import os
from hyperliquid_sdk import HyperCore

ENDPOINT = os.environ.get("ENDPOINT")
if not ENDPOINT:
    print("Set ENDPOINT environment variable")
    exit(1)

hc = HyperCore(ENDPOINT)

print("=" * 50)
print("HyperCore Block Data")
print("=" * 50)

# Latest block number
print("\n1. Latest Block:")
block_num = hc.latest_block_number()
print(f"   Block #{block_num}")

# Recent trades
print("\n2. Recent Trades (all coins):")
trades = hc.latest_trades(count=5)
for t in trades[:5]:
    side = "BUY" if t["side"] == "B" else "SELL"
    print(f"   {side} {t['sz']} {t['coin']} @ ${t['px']}")

# Recent BTC trades only
print("\n3. BTC Trades:")
btc_trades = hc.latest_trades(count=10, coin="BTC")
for t in btc_trades[:3]:
    side = "BUY" if t["side"] == "B" else "SELL"
    print(f"   {side} {t['sz']} @ ${t['px']}")
if not btc_trades:
    print("   No BTC trades in recent blocks")

# Get a specific block
print("\n4. Get Block Data:")
block = hc.get_block(block_num - 1)
print(f"   Block #{block_num - 1}")
print(f"   Time: {block.get('block_time', 'N/A')}")
print(f"   Events: {len(block.get('events', []))}")

# Get batch of blocks
print("\n5. Batch Blocks:")
blocks = hc.get_batch_blocks(block_num - 5, block_num - 1)
print(f"   Retrieved {len(blocks.get('blocks', []))} blocks")

print("\n" + "=" * 50)
print("Done!")
