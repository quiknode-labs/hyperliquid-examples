"""
Modify Order Example

Place a resting order and then modify its price.
"""

from hyperliquid_sdk import HyperliquidSDK

sdk = HyperliquidSDK()

# Place a resting order
mid = sdk.get_mid("BTC")
limit_price = int(mid * 0.97)
order = sdk.buy("BTC", notional=11, price=limit_price, tif="gtc")
print(f"Placed order at ${limit_price:,}")
print(f"  OID: {order.oid}")

# Modify to a new price (4% below mid)
new_price = int(mid * 0.96)
new_order = order.modify(price=new_price)
print(f"Modified to ${new_price:,}")
print(f"  New OID: {new_order.oid}")

# Clean up
new_order.cancel()
print("Order cancelled.")
