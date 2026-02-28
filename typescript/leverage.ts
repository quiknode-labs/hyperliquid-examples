#!/usr/bin/env npx ts-node
/**
 * Leverage Example
 *
 * Update leverage for a position.
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
  console.log(`Wallet: ${sdk.address}`);

  // Update leverage for BTC to 10x cross margin
  const result = await sdk.updateLeverage("BTC", 10, { isCross: true });
  console.log(`Update leverage result: ${JSON.stringify(result)}`);

  // Update leverage for ETH to 5x isolated margin
  // const result = await sdk.updateLeverage("ETH", 5, { isCross: false });
  // console.log(`Update leverage result: ${JSON.stringify(result)}`);

  console.log("\nLeverage methods available:");
  console.log("  sdk.updateLeverage(asset, leverage, { isCross: true })");
}

main().catch(console.error);
