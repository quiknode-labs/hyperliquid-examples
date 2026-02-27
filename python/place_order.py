"""
Limit Order Example

Place a limit order that rests on the book until filled or cancelled.
"""

from hyperliquid_sdk import HyperliquidSDK

sdk = HyperliquidSDK()

# Get current price
mid = sdk.get_mid("BTC")
print(f"BTC mid price: ${mid:,.2f}")

# Place limit buy 3% below mid (GTC = Good Till Cancelled)
limit_price = int(mid * 0.97)
order = sdk.buy("BTC", notional=11, price=limit_price, tif="gtc")

print(f"Placed limit order:")
print(f"  OID: {order.oid}")
print(f"  Price: ${limit_price:,}")
print(f"  Status: {order.status}")

# Clean up - cancel the order
order.cancel()
print("Order cancelled.")
