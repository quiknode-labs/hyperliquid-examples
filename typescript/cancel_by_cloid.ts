#!/usr/bin/env npx ts-node
/**
 * Cancel by Client Order ID (CLOID) Example
 *
 * Cancel an order using a client-provided order ID instead of the exchange OID.
 * Useful when you track orders by your own IDs.
 */

import { HyperliquidSDK } from 'hyperliquid-sdk';

async function main() {
  const sdk = new HyperliquidSDK();

  // Note: CLOIDs are hex strings you provide when placing orders
  // This example shows the cancelByCloid API

  // Cancel by client order ID
  // await sdk.cancelByCloid("0x1234567890abcdef...", "BTC");

  console.log("cancelByCloid() cancels orders by your custom client order ID");
  console.log("Usage: sdk.cancelByCloid(cloid, asset)");
}

main().catch(console.error);
