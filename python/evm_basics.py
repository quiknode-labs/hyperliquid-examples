#!/usr/bin/env python3
"""
HyperEVM Example

Shows how to use standard Ethereum JSON-RPC calls on Hyperliquid's EVM chain.

Setup:
    pip install hyperliquid-sdk

Usage:
    export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
    python evm_basics.py
"""

import os
from hyperliquid_sdk import EVM

ENDPOINT = os.environ.get("ENDPOINT")
if not ENDPOINT:
    print("Set ENDPOINT environment variable")
    exit(1)

evm = EVM(ENDPOINT)

print("=" * 50)
print("HyperEVM (Ethereum JSON-RPC)")
print("=" * 50)

# Chain info
print("\n1. Chain Info:")
chain_id = evm.chain_id()
block_num = evm.block_number()
gas_price = evm.gas_price()
print(f"   Chain ID: {chain_id}")
print(f"   Block: {block_num}")
print(f"   Gas Price: {gas_price / 1e9:.2f} gwei")

# Latest block
print("\n2. Latest Block:")
block = evm.get_block_by_number("latest")
if block:
    print(f"   Hash: {block['hash'][:20]}...")
    print(f"   Txs: {len(block.get('transactions', []))}")

# Check balance
print("\n3. Balance Check:")
addr = "0x0000000000000000000000000000000000000000"
balance = evm.get_balance(addr)
print(f"   {addr[:12]}...: {balance / 1e18:.6f} ETH")

print("\n" + "=" * 50)
print("Done!")
print("\nFor debug/trace APIs, use: EVM(endpoint, debug=True)")
