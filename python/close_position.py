"""
Close Position Example

Close an open position completely. The SDK figures out the size and direction.
"""

from hyperliquid_sdk import HyperliquidSDK

sdk = HyperliquidSDK()

# Close BTC position (if any)
# The SDK queries your position and builds the counter-order automatically
try:
    result = sdk.close_position("BTC")
    print(f"Closed position: {result}")
except Exception as e:
    print(f"No position to close or error: {e}")
