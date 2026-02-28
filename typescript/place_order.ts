#!/usr/bin/env npx ts-node
/**
 * Limit Order Example
 *
 * Place a limit order that rests on the book until filled or cancelled.
 */

import { HyperliquidSDK } from 'hyperliquid-sdk';

async function main() {
  const sdk = new HyperliquidSDK();

  // Get current price
  const mid = await sdk.getMid("BTC");
  console.log(`BTC mid price: $${mid.toLocaleString()}`);

  // Place limit buy 3% below mid (GTC = Good Till Cancelled)
  const limitPrice = Math.floor(mid * 0.97);
  const order = await sdk.buy("BTC", { notional: 11, price: limitPrice, tif: "gtc" });

  console.log("Placed limit order:");
  console.log(`  OID: ${order.oid}`);
  console.log(`  Price: $${limitPrice.toLocaleString()}`);
  console.log(`  Status: ${order.status}`);

  // Clean up - cancel the order
  await order.cancel();
  console.log("Order cancelled.");
}

main().catch(console.error);
