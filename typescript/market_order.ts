#!/usr/bin/env npx ts-node
/**
 * Market Order Example
 *
 * Place a market order that executes immediately at best available price.
 */

import { HyperliquidSDK } from 'hyperliquid-sdk';

async function main() {
  const sdk = new HyperliquidSDK();

  // Market buy by notional ($11 worth of BTC - minimum is $10)
  const order = await sdk.marketBuy("BTC", { notional: 11 });
  console.log(`Market buy: ${order}`);
  console.log(`  Status: ${order.status}`);
  console.log(`  OID: ${order.oid}`);

  // Market buy by notional ($10 worth of ETH)
  // const order = await sdk.marketBuy("ETH", { notional: 10 });

  // Market sell
  // const order = await sdk.marketSell("BTC", { size: 0.0001 });
}

main().catch(console.error);
