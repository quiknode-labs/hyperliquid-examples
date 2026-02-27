"""
Isolated Margin Example

Add or remove margin from an isolated position.

Requires: PRIVATE_KEY environment variable
"""

import os
from hyperliquid_sdk import HyperliquidSDK

private_key = os.environ.get("PRIVATE_KEY")
if not private_key:
    print("Set PRIVATE_KEY environment variable")
    print("Example: export PRIVATE_KEY='0x...'")
    exit(1)

sdk = HyperliquidSDK(private_key=private_key)
print(f"Wallet: {sdk.address}")

# Add $100 margin to BTC long position (is_buy=True for long)
# result = sdk.update_isolated_margin("BTC", amount=100, is_buy=True)
# print(f"Add margin result: {result}")

# Remove $50 margin from ETH short position (is_buy=False for short)
# result = sdk.update_isolated_margin("ETH", amount=-50, is_buy=False)
# print(f"Remove margin result: {result}")

# Top up isolated-only margin (special maintenance mode)
# result = sdk.top_up_isolated_only_margin("BTC", amount=100)
# print(f"Top up isolated-only margin result: {result}")

print("\nIsolated margin methods available:")
print("  sdk.update_isolated_margin(asset, amount=, is_buy=True)")
print("  sdk.top_up_isolated_only_margin(asset, amount=)")
