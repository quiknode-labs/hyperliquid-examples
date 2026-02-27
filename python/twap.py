"""
TWAP Orders Example

Time-Weighted Average Price orders for large trades.

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
mid = sdk.get_mid("BTC")
print(f"BTC mid: ${mid:,.2f}")

# TWAP order - executes over time to minimize market impact
# result = sdk.twap_order(
#     "BTC",
#     size=0.01,           # Total size to execute
#     is_buy=True,
#     duration_minutes=60,  # Execute over 60 minutes
#     randomize=True,       # Randomize execution times
#     reduce_only=False
# )
# print(f"TWAP order: {result}")
# twap_id = result.get("response", {}).get("data", {}).get("running", {}).get("id")

# Cancel TWAP order
# result = sdk.twap_cancel("BTC", twap_id)
# print(f"TWAP cancel: {result}")

print("\nTWAP methods available:")
print("  sdk.twap_order(asset, size=, is_buy=, duration_minutes=, randomize=True, reduce_only=False)")
print("  sdk.twap_cancel(asset, twap_id)")
