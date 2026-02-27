"""
Withdraw Example

Withdraw USDC to L1 (Arbitrum).

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

# Withdraw USDC to L1 (Arbitrum)
# WARNING: This is a real withdrawal - be careful with amounts
# result = sdk.withdraw(
#     destination="0x1234567890123456789012345678901234567890",  # Arbitrum address
#     amount=100.0
# )
# print(f"Withdraw: {result}")

print("Withdraw methods available:")
print("  sdk.withdraw(destination, amount)")
print("  Note: Withdraws USDC to your L1 Arbitrum address")
