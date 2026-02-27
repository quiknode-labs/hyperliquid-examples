"""
Cancel Order Example

Place an order and then cancel it by OID.
"""

from hyperliquid_sdk import HyperliquidSDK

sdk = HyperliquidSDK()

# Place a resting order 3% below mid
mid = sdk.get_mid("BTC")
limit_price = int(mid * 0.97)
order = sdk.buy("BTC", notional=11, price=limit_price, tif="gtc")
print(f"Placed order OID: {order.oid}")

# Cancel using the order object
order.cancel()
print("Cancelled via order.cancel()")

# Alternative: cancel by OID directly
# sdk.cancel(oid=12345, asset="BTC")
