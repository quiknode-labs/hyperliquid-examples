"""
Round Trip Example

Complete trade cycle: buy then sell to end up flat.
"""

from hyperliquid_sdk import HyperliquidSDK

sdk = HyperliquidSDK()

# Buy $11 worth of BTC
print("Buying BTC...")
buy = sdk.market_buy("BTC", notional=11)
print(f"  Bought: {buy.filled_size or buy.size} BTC")
print(f"  Status: {buy.status}")

# Sell the same amount
print("Selling BTC...")
sell = sdk.market_sell("BTC", size=buy.filled_size or buy.size)
print(f"  Sold: {sell.filled_size or sell.size} BTC")
print(f"  Status: {sell.status}")

print("Done! Position should be flat.")
