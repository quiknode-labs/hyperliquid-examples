"""
Preflight Validation Example

Validate an order BEFORE signing to catch tick size and lot size errors.
Saves failed transactions by checking validity upfront.

No endpoint or private key needed — uses public API.
"""

from hyperliquid_sdk import HyperliquidSDK

# No endpoint or private key needed for read-only public queries
sdk = HyperliquidSDK()

# Get current price
mid = sdk.get_mid("BTC")
print(f"BTC mid: ${mid:,.2f}")

# Validate a good order
result = sdk.preflight("BTC", "buy", price=int(mid * 0.97), size=0.001)
print(f"Valid order: {result}")

# Validate an order with too many decimals (will fail)
result = sdk.preflight("BTC", "buy", price=67000.123456789, size=0.001)
print(f"Invalid price: {result}")
if not result.get("valid"):
    print(f"  Error: {result.get('error')}")
    print(f"  Suggestion: {result.get('suggestion')}")
