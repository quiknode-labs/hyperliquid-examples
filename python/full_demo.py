"""
Full SDK Demo

Demonstrates all SDK capabilities in one file.
"""

from hyperliquid_sdk import HyperliquidSDK, Order

# ============================================================================
# INITIALIZATION
# ============================================================================

# Simple init (uses PRIVATE_KEY env var)
sdk = HyperliquidSDK()

# Alternative: with auto-approval
# sdk = HyperliquidSDK(auto_approve=True)

# Alternative: explicit key
# sdk = HyperliquidSDK(private_key="0x...")

print(f"Wallet: {sdk.address}\n")

# ============================================================================
# MARKET DATA
# ============================================================================

print("=== Market Data ===")

mid = sdk.get_mid("BTC")
print(f"BTC mid: ${mid:,.2f}")

markets = sdk.markets()
print(f"Perp markets: {len(markets.get('perps', []))}")
print(f"Spot markets: {len(markets.get('spot', []))}")

dexes = sdk.dexes()
print(f"HIP-3 DEXes: {len(dexes.get('dexes', []))}")

# ============================================================================
# APPROVAL STATUS
# ============================================================================

print("\n=== Approval Status ===")

status = sdk.approval_status()
print(f"Approved: {status.get('approved', False)}")
if status.get("approved"):
    print(f"Max fee: {status.get('maxFeeRate')}")

# ============================================================================
# ORDER VALIDATION (PREFLIGHT)
# ============================================================================

print("\n=== Preflight Validation ===")

result = sdk.preflight("BTC", "buy", price=int(mid * 0.97), size=0.001)
print(f"Valid order: {result.get('valid', True)}")

# ============================================================================
# OPEN ORDERS
# ============================================================================

print("\n=== Open Orders ===")

orders = sdk.open_orders()
print(f"Open orders: {orders['count']}")

for o in orders["orders"][:3]:
    side = "BUY" if o["side"] == "B" else "SELL"
    print(f"  {o['name']} {side} {o['sz']} @ {o['limitPx']} (OID: {o['oid']})")

# ============================================================================
# ORDER PLACEMENT (commented to avoid real trades)
# ============================================================================

print("\n=== Order Methods ===")
print("Available order methods:")
print("  sdk.buy(asset, size=, notional=, price=, tif=)")
print("  sdk.sell(asset, size=, notional=, price=, tif=)")
print("  sdk.market_buy(asset, size=, notional=)")
print("  sdk.market_sell(asset, size=, notional=)")
print("  sdk.long(...)  # alias for buy")
print("  sdk.short(...) # alias for sell")
print("  sdk.order(Order.buy(...).size(...).price(...).gtc())")

# ============================================================================
# ORDER MANAGEMENT (commented to avoid real actions)
# ============================================================================

print("\n=== Order Management ===")
print("Available management methods:")
print("  order.cancel()                    # Cancel via order object")
print("  order.modify(price=, size=)       # Modify via order object")
print("  sdk.cancel(oid, asset=)           # Cancel by OID")
print("  sdk.cancel_by_cloid(cloid, asset) # Cancel by client order ID")
print("  sdk.cancel_all()                  # Cancel all orders")
print("  sdk.cancel_all('BTC')             # Cancel all BTC orders")
print("  sdk.schedule_cancel(time_ms)      # Dead-man's switch")
print("  sdk.close_position('BTC')         # Close a position")

# ============================================================================
# FLUENT ORDER BUILDER
# ============================================================================

print("\n=== Fluent Order Builder ===")
print("Order.buy('BTC')")
print("  .size(0.001)       # Size in asset units")
print("  .notional(100)     # Size in USD")
print("  .price(65000)      # Limit price")
print("  .gtc()             # Good Till Cancelled")
print("  .ioc()             # Immediate Or Cancel")
print("  .alo()             # Add Liquidity Only")
print("  .market()          # Market order")
print("  .reduce_only()     # Only close position")

print("\n=== Demo Complete ===")
