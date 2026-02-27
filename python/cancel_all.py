"""
Cancel All Orders Example

Cancel all open orders, or all orders for a specific asset.
"""

from hyperliquid_sdk import HyperliquidSDK

sdk = HyperliquidSDK()

# Check open orders first
orders = sdk.open_orders()
print(f"Open orders: {orders['count']}")

# Cancel all orders
result = sdk.cancel_all()
print(f"Cancel all: {result}")

# Or cancel just BTC orders:
# sdk.cancel_all("BTC")
