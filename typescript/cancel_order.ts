#!/usr/bin/env npx ts-node
/**
 * Cancel Order Example
 *
 * Place an order and then cancel it by OID.
 */

import { HyperliquidSDK } from 'hyperliquid-sdk';

async function main() {
  const sdk = new HyperliquidSDK();

  // Place a resting order 3% below mid
  const mid = await sdk.getMid("BTC");
  const limitPrice = Math.floor(mid * 0.97);
  const order = await sdk.buy("BTC", { notional: 11, price: limitPrice, tif: "gtc" });
  console.log(`Placed order OID: ${order.oid}`);

  // Cancel using the order object
  await order.cancel();
  console.log("Cancelled via order.cancel()");

  // Alternative: cancel by OID directly
  // await sdk.cancel(12345, "BTC");
}

main().catch(console.error);
