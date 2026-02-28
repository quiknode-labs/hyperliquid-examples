#!/usr/bin/env npx ts-node
/**
 * Isolated Margin Example
 *
 * Add or remove margin from an isolated position.
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

  // Add $100 margin to BTC long position (isBuy=true for long)
  // const result = await sdk.updateIsolatedMargin("BTC", { amount: 100, isBuy: true });
  // console.log(`Add margin result: ${JSON.stringify(result)}`);

  // Remove $50 margin from ETH short position (isBuy=false for short)
  // const result = await sdk.updateIsolatedMargin("ETH", { amount: -50, isBuy: false });
  // console.log(`Remove margin result: ${JSON.stringify(result)}`);

  // Top up isolated-only margin (special maintenance mode)
  // const result = await sdk.topUpIsolatedOnlyMargin("BTC", { amount: 100 });
  // console.log(`Top up isolated-only margin result: ${JSON.stringify(result)}`);

  console.log("\nIsolated margin methods available:");
  console.log("  sdk.updateIsolatedMargin(asset, { amount, isBuy })");
  console.log("  sdk.topUpIsolatedOnlyMargin(asset, { amount })");
}

main().catch(console.error);
