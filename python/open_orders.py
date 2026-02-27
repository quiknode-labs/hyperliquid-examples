"""
Open Orders Example

View all open orders with details.
"""

from hyperliquid_sdk import HyperliquidSDK

sdk = HyperliquidSDK()

# Get all open orders
result = sdk.open_orders()
print(f"Open orders: {result['count']}")

for o in result["orders"]:
    side = "BUY" if o["side"] == "B" else "SELL"
    print(f"  {o['name']} {side} {o['sz']} @ {o['limitPx']} (OID: {o['oid']})")

# Get order status for a specific order
# status = sdk.order_status(oid=12345)
# print(f"Order status: {status}")
