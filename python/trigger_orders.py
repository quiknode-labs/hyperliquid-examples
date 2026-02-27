"""
Trigger Orders Example

Stop loss and take profit orders.

Requires: PRIVATE_KEY environment variable
"""

import os
from hyperliquid_sdk import HyperliquidSDK, Side

private_key = os.environ.get("PRIVATE_KEY")
if not private_key:
    print("Set PRIVATE_KEY environment variable")
    print("Example: export PRIVATE_KEY='0x...'")
    exit(1)

sdk = HyperliquidSDK(private_key=private_key)
mid = sdk.get_mid("BTC")
print(f"BTC mid: ${mid:,.2f}")

# Stop loss order (market) - triggers when price falls below stop price
# No limit_price means market order when triggered
# result = sdk.stop_loss(
#     "BTC",
#     size=0.001,
#     trigger_price=mid * 0.95,  # 5% below current
# )
# print(f"Stop loss (market): {result}")

# Stop loss order (limit) - triggers and places limit order at limit_price
# result = sdk.stop_loss(
#     "BTC",
#     size=0.001,
#     trigger_price=mid * 0.95,
#     limit_price=mid * 0.94,
# )
# print(f"Stop loss (limit): {result}")

# Take profit order (market) - triggers when price rises above trigger
# result = sdk.take_profit(
#     "BTC",
#     size=0.001,
#     trigger_price=mid * 1.05,  # 5% above current
# )
# print(f"Take profit (market): {result}")

# Take profit order (limit)
# result = sdk.take_profit(
#     "BTC",
#     size=0.001,
#     trigger_price=mid * 1.05,
#     limit_price=mid * 1.06,
# )
# print(f"Take profit (limit): {result}")

# For buy-side stop/TP (e.g., closing a short position), use side=Side.BUY
# result = sdk.stop_loss("BTC", size=0.001, trigger_price=mid * 1.05, side=Side.BUY)

print("\nTrigger order methods available:")
print("  sdk.stop_loss(asset, size=, trigger_price=, limit_price=None, side=Side.SELL)")
print("  sdk.take_profit(asset, size=, trigger_price=, limit_price=None, side=Side.SELL)")
print("  sdk.trigger_order(TriggerOrder(...))")
print("\nNote: Omit limit_price for market orders when triggered")
