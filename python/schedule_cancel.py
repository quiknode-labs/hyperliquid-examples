"""
Schedule Cancel Example (Dead Man's Switch)

Schedule automatic cancellation of all orders after a delay.
If you don't send another schedule_cancel before the time expires,
all your orders are cancelled. Useful as a safety mechanism.

NOTE: Requires $1M trading volume on your account to use this feature.
"""

import time
from hyperliquid_sdk import HyperliquidSDK

sdk = HyperliquidSDK()

# Schedule cancel all orders in 60 seconds
cancel_time = int(time.time() * 1000) + 60000  # 60 seconds from now
result = sdk.schedule_cancel(cancel_time)
print(f"Scheduled cancel at {cancel_time}: {result}")

# To cancel the scheduled cancel (keep orders alive):
result = sdk.schedule_cancel(None)
print(f"Cancelled scheduled cancel: {result}")
