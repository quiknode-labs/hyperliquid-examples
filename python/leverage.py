"""
Leverage Example

Update leverage for a position.

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

# Update leverage for BTC to 10x cross margin
result = sdk.update_leverage("BTC", leverage=10, is_cross=True)
print(f"Update leverage result: {result}")

# Update leverage for ETH to 5x isolated margin
# result = sdk.update_leverage("ETH", leverage=5, is_cross=False)
# print(f"Update leverage result: {result}")

print("\nLeverage methods available:")
print("  sdk.update_leverage(asset, leverage=, is_cross=True)")
