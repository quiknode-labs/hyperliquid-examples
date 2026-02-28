#!/usr/bin/env npx ts-node
/**
 * Market Data Example
 *
 * Shows how to query market metadata, prices, order book, and recent trades.
 *
 * The SDK handles all Info API methods automatically.
 *
 * Setup:
 *     npm install hyperliquid-sdk
 *
 * Usage:
 *     export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
 *     npx ts-node info_market_data.ts
 */

import { HyperliquidSDK, HyperliquidError } from 'hyperliquid-sdk';

const ENDPOINT = process.env.ENDPOINT;
if (!ENDPOINT) {
  console.log("Set ENDPOINT environment variable");
  console.log("Example: export ENDPOINT='https://your-endpoint.hype-mainnet.quiknode.pro/TOKEN'");
  process.exit(1);
}

async function main() {
  // Single SDK instance — access everything through sdk.info, sdk.core, sdk.evm, etc.
  const sdk = new HyperliquidSDK(ENDPOINT);
  const info = sdk.info;

  console.log("=".repeat(50));
  console.log("Market Data (Info API)");
  console.log("=".repeat(50));

  // Exchange metadata
  console.log("\n1. Exchange Metadata:");
  try {
    const meta = await info.meta() as Record<string, unknown>;
    const universe = (meta.universe || []) as unknown[];
    console.log(`   Perp Markets: ${universe.length}`);
    for (const asset of universe.slice(0, 5)) {
      const a = asset as Record<string, unknown>;
      console.log(`   - ${a.name}: max leverage ${a.maxLeverage}x`);
    }
  } catch (e) {
    if (e instanceof HyperliquidError) {
      console.log(`   (meta not available: ${e.code})`);
    }
  }

  // Spot metadata
  console.log("\n2. Spot Metadata:");
  try {
    const spot = await info.spotMeta() as Record<string, unknown>;
    console.log(`   Spot Tokens: ${((spot.tokens || []) as unknown[]).length}`);
  } catch (e) {
    if (e instanceof HyperliquidError) {
      console.log(`   (spotMeta not available: ${(e as HyperliquidError).code})`);
    }
  }

  // Exchange status
  console.log("\n3. Exchange Status:");
  try {
    const status = await info.exchangeStatus();
    console.log(`   ${JSON.stringify(status)}`);
  } catch (e) {
    if (e instanceof HyperliquidError) {
      console.log(`   (exchangeStatus not available: ${(e as HyperliquidError).code})`);
    }
  }

  // All mid prices
  console.log("\n4. Mid Prices:");
  try {
    const mids = await info.allMids() as Record<string, string>;
    console.log(`   BTC: $${parseFloat(mids.BTC || '0').toLocaleString()}`);
    console.log(`   ETH: $${parseFloat(mids.ETH || '0').toLocaleString()}`);
  } catch (e) {
    if (e instanceof HyperliquidError) {
      console.log(`   (allMids not available: ${(e as HyperliquidError).code})`);
    }
  }

  // Order book
  console.log("\n5. Order Book (BTC):");
  try {
    const book = await info.l2Book("BTC") as Record<string, unknown>;
    const levels = (book.levels || [[], []]) as unknown[][];
    if (levels[0]?.length && levels[1]?.length) {
      const bid0 = levels[0][0] as Record<string, unknown>;
      const ask0 = levels[1][0] as Record<string, unknown>;
      const bestBid = parseFloat(String(bid0.px || 0));
      const bestAsk = parseFloat(String(ask0.px || 0));
      const spread = bestAsk - bestBid;
      console.log(`   Best Bid: $${bestBid.toLocaleString()}`);
      console.log(`   Best Ask: $${bestAsk.toLocaleString()}`);
      console.log(`   Spread: $${spread.toFixed(2)}`);
    }
  } catch (e) {
    if (e instanceof HyperliquidError) {
      console.log(`   (l2Book not available: ${(e as HyperliquidError).code})`);
    }
  }

  // Recent trades
  console.log("\n6. Recent Trades (BTC):");
  try {
    const trades = await info.recentTrades("BTC") as unknown[];
    for (const t of trades.slice(0, 3)) {
      const trade = t as Record<string, unknown>;
      const side = trade.side === "B" ? "BUY" : "SELL";
      console.log(`   ${side} ${trade.sz} @ $${parseFloat(String(trade.px || 0)).toLocaleString()}`);
    }
  } catch (e) {
    if (e instanceof HyperliquidError) {
      console.log(`   (recentTrades not available: ${(e as HyperliquidError).code})`);
    }
  }

  console.log("\n" + "=".repeat(50));
  console.log("Done!");
}

main().catch(console.error);
