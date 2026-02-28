#!/usr/bin/env npx ts-node
/**
 * Markets Example
 *
 * List all available markets and HIP-3 DEXes.
 *
 * No endpoint or private key needed — uses public API.
 */

import { HyperliquidSDK } from 'hyperliquid-sdk';

async function main() {
  // No endpoint or private key needed for read-only public queries
  const sdk = new HyperliquidSDK();

  // Get all markets
  const markets = await sdk.markets() as Record<string, unknown>;
  console.log(`Perp markets: ${((markets.perps || []) as unknown[]).length}`);
  console.log(`Spot markets: ${((markets.spot || []) as unknown[]).length}`);

  // Show first 5 perp markets
  console.log("\nFirst 5 perp markets:");
  for (const m of ((markets.perps || []) as unknown[]).slice(0, 5)) {
    const market = m as Record<string, unknown>;
    console.log(`  ${market.name}: szDecimals=${market.szDecimals}`);
  }

  // Get HIP-3 DEXes
  const dexesResponse = await sdk.dexes();
  const dexesList = Array.isArray(dexesResponse)
    ? dexesResponse
    : Object.values(dexesResponse);
  console.log(`\nHIP-3 DEXes: ${dexesList.length}`);
  for (const dex of dexesList.slice(0, 5)) {
    console.log(`  ${(dex as Record<string, unknown>).name || JSON.stringify(dex)}`);
  }
}

main().catch(console.error);
