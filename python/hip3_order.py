"""
HIP-3 Market Order Example

Trade on HIP-3 markets (community perps like Hypersea).
Same API as regular markets, just use "dex:symbol" format.
"""

from hyperliquid_sdk import HyperliquidSDK

sdk = HyperliquidSDK()

# List HIP-3 DEXes
dexes = sdk.dexes()
print("Available HIP-3 DEXes:")
for dex in dexes[:5]:
    print(f"  {dex.get('name', dex)}")

# Trade on a HIP-3 market
# Format: "dex:SYMBOL"
# order = sdk.buy("xyz:SILVER", notional=11, tif="ioc")
# print(f"HIP-3 order: {order}")

print("\nHIP-3 markets use 'dex:SYMBOL' format")
print("Example: sdk.buy('xyz:SILVER', notional=11)")
