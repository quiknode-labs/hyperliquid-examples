"""
Market Order Example

Place a market order that executes immediately at best available price.
"""

from hyperliquid_sdk import HyperliquidSDK

sdk = HyperliquidSDK()

# Market buy by size (0.0001 BTC)
order = sdk.market_buy("BTC", size=0.0001)
print(f"Market buy: {order}")
print(f"  Status: {order.status}")
print(f"  OID: {order.oid}")

# Market buy by notional ($10 worth of ETH)
# order = sdk.market_buy("ETH", notional=10)

# Market sell
# order = sdk.market_sell("BTC", size=0.0001)
