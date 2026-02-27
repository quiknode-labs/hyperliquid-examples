"""
Markets Example

List all available markets and HIP-3 DEXes.

No endpoint or private key needed — uses public API.
"""

from hyperliquid_sdk import HyperliquidSDK

# No endpoint or private key needed for read-only public queries
sdk = HyperliquidSDK()

# Get all markets
markets = sdk.markets()
print(f"Perp markets: {len(markets.get('perps', []))}")
print(f"Spot markets: {len(markets.get('spot', []))}")

# Show first 5 perp markets
print("\nFirst 5 perp markets:")
for m in markets.get("perps", [])[:5]:
    print(f"  {m['name']}: szDecimals={m.get('szDecimals')}")

# Get HIP-3 DEXes
dexes = sdk.dexes()
print(f"\nHIP-3 DEXes: {len(dexes)}")
for dex in dexes[:5]:
    print(f"  {dex.get('name', 'N/A')}")
