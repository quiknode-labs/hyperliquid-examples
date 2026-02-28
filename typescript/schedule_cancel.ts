#!/usr/bin/env npx ts-node
/**
 * Schedule Cancel Example (Dead Man's Switch)
 *
 * Schedule automatic cancellation of all orders after a delay.
 * If you don't send another scheduleCancel before the time expires,
 * all your orders are cancelled. Useful as a safety mechanism.
 *
 * NOTE: Requires $1M trading volume on your account to use this feature.
 */

import { HyperliquidSDK } from 'hyperliquid-sdk';

async function main() {
  const sdk = new HyperliquidSDK();

  // Schedule cancel all orders in 60 seconds
  // const cancelTime = Date.now() + 60000;  // 60 seconds from now
  // const result = await sdk.scheduleCancel(cancelTime);
  // console.log(`Scheduled cancel at ${cancelTime}: ${JSON.stringify(result)}`);

  // To cancel the scheduled cancel (keep orders alive):
  // const result = await sdk.scheduleCancel();
  // console.log(`Cancelled scheduled cancel: ${JSON.stringify(result)}`);

  console.log("Schedule cancel methods available:");
  console.log("  sdk.scheduleCancel(timeMs)  // Schedule cancel at timestamp");
  console.log("  sdk.scheduleCancel()        // Cancel the scheduled cancel");
  console.log("\nNOTE: Requires $1M trading volume on your account");
}

main().catch(console.error);
