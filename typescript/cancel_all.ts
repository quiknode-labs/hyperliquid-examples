#!/usr/bin/env npx ts-node
/**
 * Cancel All Orders Example
 *
 * Cancel all open orders, or all orders for a specific asset.
 */

import { HyperliquidSDK } from 'hyperliquid-sdk';

async function main() {
  const sdk = new HyperliquidSDK();

  // Check open orders first
  const orders = await sdk.openOrders();
  console.log(`Open orders: ${(orders as any).count}`);

  // Cancel all orders
  const result = await sdk.cancelAll();
  console.log(`Cancel all: ${JSON.stringify(result)}`);

  // Or cancel just BTC orders:
  // await sdk.cancelAll("BTC");
}

main().catch(console.error);
