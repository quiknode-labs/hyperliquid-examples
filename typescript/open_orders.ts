#!/usr/bin/env npx ts-node
/**
 * Open Orders Example
 *
 * View all open orders with details.
 *
 * Requires: PRIVATE_KEY environment variable
 */

import { HyperliquidSDK } from 'hyperliquid-sdk';

async function main() {
  // Private key required to query your open orders
  const privateKey = process.env.PRIVATE_KEY;
  if (!privateKey) {
    console.log("Set PRIVATE_KEY environment variable");
    console.log("Example: export PRIVATE_KEY='0x...'");
    process.exit(1);
  }

  const sdk = new HyperliquidSDK(undefined, { privateKey });

  // Get all open orders
  const result = await sdk.openOrders() as Record<string, unknown>;
  console.log(`Open orders: ${result.count}`);

  for (const o of (result.orders || []) as unknown[]) {
    const order = o as Record<string, unknown>;
    const side = order.side === "B" ? "BUY" : "SELL";
    console.log(`  ${order.name} ${side} ${order.sz} @ ${order.limitPx} (OID: ${order.oid})`);
  }

  // Get order status for a specific order
  // const status = await sdk.orderStatus(12345);
  // console.log(`Order status: ${JSON.stringify(status)}`);
}

main().catch(console.error);
