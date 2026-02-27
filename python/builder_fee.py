"""
Builder Fee Example

Approve and revoke builder fee permissions.

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

# Check approval status (doesn't require deposit)
status = sdk.approval_status()
print(f"Approval status: {status}")

# Approve builder fee (required before trading via QuickNode)
# Note: Requires account to have deposited first
# result = sdk.approve_builder_fee(max_fee="1%")
# print(f"Approve builder fee: {result}")

# Revoke builder fee permission
# result = sdk.revoke_builder_fee()
# print(f"Revoke builder fee: {result}")

print("\nBuilder fee methods available:")
print("  sdk.approve_builder_fee(max_fee='1%', builder=None)")
print("  sdk.revoke_builder_fee(builder=None)")
print("  sdk.approval_status(user=None)")
