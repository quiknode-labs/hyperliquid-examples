"""
Transfers Example

Transfer USD and spot assets between accounts and wallets.

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

# Transfer USD to another address
# result = sdk.transfer_usd(
#     destination="0x1234567890123456789012345678901234567890",
#     amount=10.0
# )
# print(f"USD transfer: {result}")

# Transfer spot asset to another address
# result = sdk.transfer_spot(
#     token="PURR",  # or token index
#     destination="0x1234567890123456789012345678901234567890",
#     amount=100.0
# )
# print(f"Spot transfer: {result}")

# Transfer from spot wallet to perp wallet (internal)
# result = sdk.transfer_spot_to_perp(amount=100.0)
# print(f"Spot to perp: {result}")

# Transfer from perp wallet to spot wallet (internal)
# result = sdk.transfer_perp_to_spot(amount=100.0)
# print(f"Perp to spot: {result}")

# Send asset (generalized transfer)
# result = sdk.send_asset(
#     token="USDC",  # or token index
#     amount="100.0",
#     destination="0x1234567890123456789012345678901234567890"
# )
# print(f"Send asset: {result}")

print("Transfer methods available:")
print("  sdk.transfer_usd(destination, amount)")
print("  sdk.transfer_spot(token, destination, amount)")
print("  sdk.transfer_spot_to_perp(amount)")
print("  sdk.transfer_perp_to_spot(amount)")
print("  sdk.send_asset(token, amount, destination)")
