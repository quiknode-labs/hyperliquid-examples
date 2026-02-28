#!/usr/bin/env npx ts-node
/**
 * HIP-3 Market Order Example
 *
 * Trade on HIP-3 markets (community perps like Hypersea).
 * Same API as regular markets, just use "dex:symbol" format.
 */

import { HyperliquidSDK } from 'hyperliquid-sdk';

async function main() {
  const sdk = new HyperliquidSDK();

  // List HIP-3 DEXes
  const dexesResponse = await sdk.dexes();
  console.log("Available HIP-3 DEXes:");
  const dexesList = Array.isArray(dexesResponse)
    ? dexesResponse
    : Object.values(dexesResponse);
  for (const dex of dexesList.slice(0, 5)) {
    const d = dex as Record<string, unknown>;
    console.log(`  ${d.name || JSON.stringify(dex)}`);
  }

  // Trade on a HIP-3 market
  // Format: "dex:SYMBOL"
  // const order = await sdk.buy("xyz:SILVER", { notional: 11, tif: "ioc" });
  // console.log(`HIP-3 order: ${order}`);

  console.log("\nHIP-3 markets use 'dex:SYMBOL' format");
  console.log("Example: sdk.buy('xyz:SILVER', { notional: 11 })");
}

main().catch(console.error);
