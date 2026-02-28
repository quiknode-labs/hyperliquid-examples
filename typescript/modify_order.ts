#!/usr/bin/env npx ts-node
/**
 * Modify Order Example
 *
 * Place a resting order and then modify its price.
 */

import { HyperliquidSDK } from 'hyperliquid-sdk';

async function main() {
  const sdk = new HyperliquidSDK();

  // Place a resting order
  const mid = await sdk.getMid("BTC");
  const limitPrice = Math.floor(mid * 0.97);
  const order = await sdk.buy("BTC", { notional: 11, price: limitPrice, tif: "gtc" });
  console.log(`Placed order at $${limitPrice.toLocaleString()}`);
  console.log(`  OID: ${order.oid}`);

  // Modify to a new price (4% below mid)
  const newPrice = Math.floor(mid * 0.96);
  const newOrder = await order.modify({ price: newPrice });
  console.log(`Modified to $${newPrice.toLocaleString()}`);
  console.log(`  New OID: ${newOrder.oid}`);

  // Clean up
  await newOrder.cancel();
  console.log("Order cancelled.");
}

main().catch(console.error);
