#!/usr/bin/env python3
"""
Vaults & Delegation Example

Shows how to query vault information and user delegations.

Setup:
    pip install hyperliquid-sdk

Usage:
    export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
    export USER_ADDRESS="0x..."  # Optional
    python info_vaults.py
"""

import os
from hyperliquid_sdk import Info

ENDPOINT = os.environ.get("ENDPOINT")
USER = os.environ.get("USER_ADDRESS")

if not ENDPOINT:
    print("Set ENDPOINT environment variable")
    exit(1)

info = Info(ENDPOINT)

print("=" * 50)
print("Vaults & Delegation")
print("=" * 50)

# Vault summaries
print("\n1. Vault Summaries:")
vaults = info.vault_summaries()
print(f"   Total: {len(vaults)}")
for v in vaults[:3]:
    print(f"   - {v.get('name', 'N/A')}: TVL ${v.get('tvl', '?')}")

# User delegations
if USER:
    print(f"\n2. Delegations ({USER[:10]}...):")
    delegations = info.delegations(USER)
    if delegations:
        print(f"   {len(delegations)} active")
    else:
        print("   None")
else:
    print("\n(Set USER_ADDRESS for delegation info)")

print("\n" + "=" * 50)
print("Done!")
