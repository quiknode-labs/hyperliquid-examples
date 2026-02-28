#!/usr/bin/env npx ts-node
/**
 * Close Position Example
 *
 * Close an open position completely. The SDK figures out the size and direction.
 */

import { HyperliquidSDK } from 'hyperliquid-sdk';

async function main() {
  const sdk = new HyperliquidSDK();

  // Close BTC position (if any)
  // The SDK queries your position and builds the counter-order automatically
  try {
    const result = await sdk.closePosition("BTC");
    console.log(`Closed position: ${JSON.stringify(result)}`);
  } catch (e) {
    console.log(`No position to close or error: ${e}`);
  }
}

main().catch(console.error);
