"""
Vaults Example

Deposit and withdraw from Hyperliquid vaults.

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

# Example vault address (HLP vault)
HLP_VAULT = "0xdfc24b077bc1425ad1dea75bcb6f8158e10df303"

# Deposit to vault
# result = sdk.vault_deposit(vault_address=HLP_VAULT, amount=100.0)
# print(f"Vault deposit: {result}")

# Withdraw from vault
# result = sdk.vault_withdraw(vault_address=HLP_VAULT, amount=50.0)
# print(f"Vault withdraw: {result}")

print("Vault methods available:")
print("  sdk.vault_deposit(vault_address, amount)")
print("  sdk.vault_withdraw(vault_address, amount)")
