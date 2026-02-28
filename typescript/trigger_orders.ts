#!/usr/bin/env npx ts-node
/**
 * Trigger Orders Example
 *
 * Stop loss and take profit orders.
 *
 * Requires: PRIVATE_KEY environment variable
 */

import { HyperliquidSDK, Side } from 'hyperliquid-sdk';

async function main() {
  const privateKey = process.env.PRIVATE_KEY;
  if (!privateKey) {
    console.log("Set PRIVATE_KEY environment variable");
    console.log("Example: export PRIVATE_KEY='0x...'");
    process.exit(1);
  }

  const sdk = new HyperliquidSDK(undefined, { privateKey });
  const mid = await sdk.getMid("BTC");
  console.log(`BTC mid: $${mid.toLocaleString()}`);

  // Stop loss order (market) - triggers when price falls below stop price
  // No limitPrice means market order when triggered
  // const result = await sdk.stopLoss("BTC", {
  //   size: 0.001,
  //   triggerPrice: mid * 0.95,  // 5% below current
  // });
  // console.log(`Stop loss (market): ${JSON.stringify(result)}`);

  // Stop loss order (limit) - triggers and places limit order at limitPrice
  // const result = await sdk.stopLoss("BTC", {
  //   size: 0.001,
  //   triggerPrice: mid * 0.95,
  //   limitPrice: mid * 0.94,
  // });
  // console.log(`Stop loss (limit): ${JSON.stringify(result)}`);

  // Take profit order (market) - triggers when price rises above trigger
  // const result = await sdk.takeProfit("BTC", {
  //   size: 0.001,
  //   triggerPrice: mid * 1.05,  // 5% above current
  // });
  // console.log(`Take profit (market): ${JSON.stringify(result)}`);

  // Take profit order (limit)
  // const result = await sdk.takeProfit("BTC", {
  //   size: 0.001,
  //   triggerPrice: mid * 1.05,
  //   limitPrice: mid * 1.06,
  // });
  // console.log(`Take profit (limit): ${JSON.stringify(result)}`);

  // For buy-side stop/TP (e.g., closing a short position), use side: Side.BUY
  // const result = await sdk.stopLoss("BTC", { size: 0.001, triggerPrice: mid * 1.05, side: Side.BUY });

  console.log("\nTrigger order methods available:");
  console.log("  sdk.stopLoss(asset, { size, triggerPrice, limitPrice?, side? })");
  console.log("  sdk.takeProfit(asset, { size, triggerPrice, limitPrice?, side? })");
  console.log("  sdk.triggerOrder(TriggerOrder(...))");
  console.log("\nNote: Omit limitPrice for market orders when triggered");
}

main().catch(console.error);
