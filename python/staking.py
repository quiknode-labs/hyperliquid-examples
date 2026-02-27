"""
Staking Example

Stake and unstake HYPE tokens.

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

# Stake HYPE tokens
# result = sdk.stake(amount=100)
# print(f"Stake: {result}")

# Unstake HYPE tokens
# result = sdk.unstake(amount=50)
# print(f"Unstake: {result}")

# Delegate to a validator
# result = sdk.delegate(
#     validator="0x...",  # Validator address
#     amount=100
# )
# print(f"Delegate: {result}")

# Undelegate from a validator
# result = sdk.undelegate(
#     validator="0x...",  # Validator address
#     amount=50
# )
# print(f"Undelegate: {result}")

print("Staking methods available:")
print("  sdk.stake(amount)")
print("  sdk.unstake(amount)")
print("  sdk.delegate(validator, amount)")
print("  sdk.undelegate(validator, amount)")
