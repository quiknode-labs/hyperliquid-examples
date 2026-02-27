"""
Cancel by Client Order ID (CLOID) Example

Cancel an order using a client-provided order ID instead of the exchange OID.
Useful when you track orders by your own IDs.
"""

from hyperliquid_sdk import HyperliquidSDK

sdk = HyperliquidSDK()

# Note: CLOIDs are hex strings you provide when placing orders
# This example shows the cancel_by_cloid API

# Cancel by client order ID
# sdk.cancel_by_cloid(cloid="0x1234567890abcdef...", asset="BTC")

print("cancel_by_cloid() cancels orders by your custom client order ID")
print("Usage: sdk.cancel_by_cloid(cloid='0x...', asset='BTC')")
