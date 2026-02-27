"""
Open Orders Example

View all open orders with details.

Requires: PRIVATE_KEY environment variable
"""

import os
from hyperliquid_sdk import HyperliquidSDK

# Private key required to query your open orders
private_key = os.environ.get("PRIVATE_KEY")
if not private_key:
    print("Set PRIVATE_KEY environment variable")
    print("Example: export PRIVATE_KEY='0x...'")
    exit(1)

sdk = HyperliquidSDK(private_key=private_key)

# Get all open orders
result = sdk.open_orders()
print(f"Open orders: {result['count']}")

for o in result["orders"]:
    side = "BUY" if o["side"] == "B" else "SELL"
    print(f"  {o['name']} {side} {o['sz']} @ {o['limitPx']} (OID: {o['oid']})")

# Get order status for a specific order
# status = sdk.order_status(oid=12345)
# print(f"Order status: {status}")
