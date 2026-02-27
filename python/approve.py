"""
Builder Fee Approval Example

Approve the builder fee to enable trading through the API.
Required before placing orders.
"""

from hyperliquid_sdk import HyperliquidSDK

sdk = HyperliquidSDK()

# Check current approval status
status = sdk.approval_status()
print(f"Currently approved: {status.get('approved', False)}")
if status.get("approved"):
    print(f"Max fee rate: {status.get('maxFeeRate')}")

# Approve builder fee (1% max)
# sdk.approve_builder_fee("1%")
# print("Approved!")

# Or use auto_approve when creating SDK:
# sdk = HyperliquidSDK(auto_approve=True)

# Revoke approval:
# sdk.revoke_builder_fee()
