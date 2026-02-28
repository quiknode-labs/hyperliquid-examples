#!/usr/bin/env npx ts-node
/**
 * TWAP Orders Example
 *
 * Time-Weighted Average Price orders for large trades.
 *
 * Requires: PRIVATE_KEY environment variable
 */

import { HyperliquidSDK } from 'hyperliquid-sdk';

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

  // TWAP order - executes over time to minimize market impact
  // const result = await sdk.twapOrder("BTC", {
  //   size: 0.01,            // Total size to execute
  //   isBuy: true,
  //   durationMinutes: 60,   // Execute over 60 minutes
  //   randomize: true,       // Randomize execution times
  //   reduceOnly: false
  // });
  // console.log(`TWAP order: ${JSON.stringify(result)}`);
  // const twapId = result?.response?.data?.running?.id;

  // Cancel TWAP order
  // const result = await sdk.twapCancel("BTC", twapId);
  // console.log(`TWAP cancel: ${JSON.stringify(result)}`);

  console.log("\nTWAP methods available:");
  console.log("  sdk.twapOrder(asset, { size, isBuy, durationMinutes, randomize?, reduceOnly? })");
  console.log("  sdk.twapCancel(asset, twapId)");
}

main().catch(console.error);
