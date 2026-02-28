#!/usr/bin/env npx ts-node
/**
 * HyperCore Block Data Example
 *
 * Shows how to get real-time trades, orders, and block data via the HyperCore API.
 *
 * This is the alternative to Info methods (allMids, l2Book, recentTrades) that
 * are not available on QuickNode endpoints.
 *
 * Setup:
 *     npm install hyperliquid-sdk
 *
 * Usage:
 *     export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
 *     npx ts-node hypercore_blocks.ts
 */

import { HyperliquidSDK } from 'hyperliquid-sdk';

const ENDPOINT = process.env.ENDPOINT;
if (!ENDPOINT) {
  console.log("Set ENDPOINT environment variable");
  process.exit(1);
}

async function main() {
  // Single SDK instance — access everything through sdk.info, sdk.core, sdk.evm, etc.
  const sdk = new HyperliquidSDK(ENDPOINT);
  const hc = sdk.core;

  console.log("=".repeat(50));
  console.log("HyperCore Block Data");
  console.log("=".repeat(50));

  // Latest block number
  console.log("\n1. Latest Block:");
  const blockNum = await hc.latestBlockNumber();
  console.log(`   Block #${blockNum.toLocaleString()}`);

  // Recent trades
  console.log("\n2. Recent Trades (all coins):");
  const trades = await hc.latestTrades({ count: 5 });
  for (const t of trades.slice(0, 5)) {
    const trade = t as Record<string, unknown>;
    const side = trade.side === "B" ? "BUY" : "SELL";
    console.log(`   ${side} ${trade.sz} ${trade.coin} @ $${trade.px}`);
  }

  // Recent BTC trades only
  console.log("\n3. BTC Trades:");
  const btcTrades = await hc.latestTrades({ count: 10, coin: "BTC" });
  for (const t of btcTrades.slice(0, 3)) {
    const trade = t as Record<string, unknown>;
    const side = trade.side === "B" ? "BUY" : "SELL";
    console.log(`   ${side} ${trade.sz} @ $${trade.px}`);
  }
  if (!btcTrades.length) {
    console.log("   No BTC trades in recent blocks");
  }

  // Get a specific block
  console.log("\n4. Get Block Data:");
  const block = await hc.getBlock(blockNum - 1) as Record<string, unknown>;
  console.log(`   Block #${blockNum - 1}`);
  console.log(`   Time: ${block.block_time || 'N/A'}`);
  console.log(`   Events: ${((block.events as unknown[]) || []).length}`);

  // Get batch of blocks
  console.log("\n5. Batch Blocks:");
  const batchResult = await hc.getBatchBlocks(blockNum - 5, blockNum - 1);
  const blocksArr = (batchResult as unknown as { blocks: unknown[] }).blocks || [];
  console.log(`   Retrieved ${blocksArr.length} blocks`);

  console.log("\n" + "=".repeat(50));
  console.log("Done!");
}

main().catch(console.error);
