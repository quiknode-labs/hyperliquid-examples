#!/usr/bin/env npx ts-node
/**
 * Full Demo — Comprehensive example of all SDK capabilities.
 *
 * This example demonstrates all major SDK features:
 * - Info API (market data, user info)
 * - HyperCore API (blocks, trades, orders)
 * - EVM API (chain data, balances)
 * - WebSocket streaming
 * - gRPC streaming
 * - Trading (orders, positions)
 *
 * Requirements:
 *     npm install hyperliquid-sdk ws @grpc/grpc-js @grpc/proto-loader
 *
 * Usage:
 *     export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/TOKEN"
 *     export PRIVATE_KEY="0x..."  # Optional, for trading
 *     npx ts-node full_demo.ts
 */

import {
  HyperliquidSDK,
  HyperliquidError,
  Stream,
  GRPCStream,
} from 'hyperliquid-sdk';

function separator(title: string): void {
  console.log();
  console.log("=".repeat(60));
  console.log(`  ${title}`);
  console.log("=".repeat(60));
}

function subsection(title: string): void {
  console.log();
  console.log(`--- ${title} ---`);
}

async function demoInfoApi(endpoint: string): Promise<void> {
  separator("INFO API");

  const sdk = new HyperliquidSDK(endpoint);
  const info = sdk.info;

  subsection("Market Prices");
  const mids = await info.allMids() as Record<string, string>;
  console.log(`Total markets: ${Object.keys(mids).length}`);
  for (const coin of ["BTC", "ETH", "SOL", "DOGE"]) {
    if (mids[coin]) {
      console.log(`  ${coin}: $${parseFloat(mids[coin]).toLocaleString()}`);
    }
  }

  subsection("Order Book");
  const book = await info.l2Book("BTC") as Record<string, unknown>;
  const levels = (book.levels || [[], []]) as unknown[][];
  const bids = levels[0] || [];
  const asks = levels[1] || [];
  if (bids.length && asks.length) {
    const bid0 = bids[0] as Record<string, unknown>;
    const ask0 = asks[0] as Record<string, unknown>;
    console.log(`  Best Bid: ${bid0.sz} @ $${parseFloat(String(bid0.px)).toLocaleString()}`);
    console.log(`  Best Ask: ${ask0.sz} @ $${parseFloat(String(ask0.px)).toLocaleString()}`);
    console.log(`  Spread: $${(parseFloat(String(ask0.px)) - parseFloat(String(bid0.px))).toLocaleString()}`);
  }

  subsection("Recent Trades");
  const trades = await info.recentTrades("ETH") as unknown[];
  console.log("Last 3 ETH trades:");
  for (const t of trades.slice(0, 3)) {
    const trade = t as Record<string, unknown>;
    console.log(`  ${trade.sz} @ $${parseFloat(String(trade.px || 0)).toLocaleString()} (${trade.side})`);
  }

  subsection("Exchange Metadata");
  const meta = await info.meta() as Record<string, unknown>;
  const universe = (meta.universe || []) as unknown[];
  console.log(`Total perp markets: ${universe.length}`);
}

async function demoHypercoreApi(endpoint: string): Promise<void> {
  separator("HYPERCORE API");

  const sdk = new HyperliquidSDK(endpoint);
  const hc = sdk.core;

  subsection("Latest Block");
  const blockNum = await hc.latestBlockNumber();
  console.log(`Latest block: ${blockNum.toLocaleString()}`);

  const block = await hc.getBlock(blockNum) as Record<string, unknown>;
  if (block) {
    const txs = (block.transactions || []) as unknown[];
    console.log(`Block ${blockNum}: ${txs.length} transactions`);
  }

  subsection("Recent Trades");
  const trades = await hc.latestTrades({ count: 5 });
  console.log("Last 5 trades across all markets:");
  for (const t of trades) {
    const trade = t as Record<string, unknown>;
    const coin = trade.coin || "?";
    console.log(`  ${coin}: ${trade.sz || '?'} @ $${parseFloat(String(trade.px || 0)).toLocaleString()}`);
  }
}

async function demoEvmApi(endpoint: string): Promise<void> {
  separator("EVM API");

  const sdk = new HyperliquidSDK(endpoint);
  const evm = sdk.evm;

  subsection("Chain Info");
  const chainId = await evm.chainId();
  const blockNum = await evm.blockNumber();
  const gasPrice = await evm.gasPrice();

  console.log(`Chain ID: ${chainId} (${chainId === 999 ? 'Mainnet' : 'Testnet'})`);
  console.log(`Block: ${blockNum.toLocaleString()}`);
  console.log(`Gas: ${(Number(gasPrice) / 1e9).toFixed(2)} Gwei`);
}

async function demoWebsocket(endpoint: string, duration: number = 5): Promise<void> {
  separator("WEBSOCKET STREAMING");

  let tradeCount = 0;
  let bookCount = 0;

  const onTrade = (data: Record<string, unknown>) => {
    tradeCount++;
    if (tradeCount <= 3) {
      const d = (data.data || {}) as Record<string, unknown>;
      console.log(`  [TRADE] ${d.coin || '?'}: ${d.sz || '?'} @ ${d.px || '?'}`);
    }
  };

  const onBook = (data: Record<string, unknown>) => {
    bookCount++;
    if (bookCount <= 2) {
      const d = (data.data || {}) as Record<string, unknown>;
      console.log(`  [BOOK] ${d.coin || '?'} update`);
    }
  };

  console.log(`Streaming for ${duration} seconds...`);

  const stream = new Stream(endpoint, { reconnect: false });
  stream.trades(["BTC", "ETH"], onTrade);
  stream.bookUpdates(["BTC"], onBook);

  await stream.start();
  await new Promise(resolve => setTimeout(resolve, duration * 1000));
  stream.stop();

  console.log();
  console.log(`Received: ${tradeCount} trades, ${bookCount} book updates`);
}

async function demoGrpc(endpoint: string, duration: number = 5): Promise<void> {
  separator("GRPC STREAMING");

  let tradeCount = 0;

  const onTrade = (data: Record<string, unknown>) => {
    tradeCount++;
    if (tradeCount <= 3) {
      console.log(`  [TRADE] ${JSON.stringify(data)}`);
    }
  };

  console.log(`Streaming for ${duration} seconds...`);

  try {
    const stream = new GRPCStream(endpoint, { reconnect: false });
    stream.trades(["BTC", "ETH"], onTrade);

    await stream.start();
    await new Promise(resolve => setTimeout(resolve, duration * 1000));
    stream.stop();

    console.log();
    console.log(`Received: ${tradeCount} trades`);
  } catch (e) {
    console.log("  gRPC not available. Install: npm install @grpc/grpc-js @grpc/proto-loader");
  }
}

async function demoTrading(endpoint: string, privateKey: string): Promise<void> {
  separator("TRADING");

  const sdk = new HyperliquidSDK(endpoint, { privateKey });

  console.log(`Address: ${sdk.address}`);
  console.log(`Endpoint: ${endpoint.slice(0, 50)}...`);

  subsection("Account Check");
  console.log("  Trading SDK initialized successfully");
  console.log("  Ready to place orders (not executing in demo)");

  subsection("Order Building (Example)");
  console.log("  Market buy: await sdk.marketBuy('BTC', { notional: 100 })");
  console.log("  Limit sell: await sdk.sell('ETH', { size: 1.0, price: 4000 })");
  console.log("  Close pos:  await sdk.closePosition('BTC')");
}

async function main(): Promise<void> {
  console.log();
  console.log("*".repeat(60));
  console.log("  HYPERLIQUID SDK - FULL DEMO");
  console.log("*".repeat(60));

  const endpoint = process.argv[2] || process.env.ENDPOINT || process.env.QUICKNODE_ENDPOINT;
  const privateKey = process.env.PRIVATE_KEY;

  if (!endpoint) {
    console.log();
    console.log("Error: ENDPOINT not set");
    console.log();
    console.log("Usage:");
    console.log("  export ENDPOINT='https://your-endpoint.hype-mainnet.quiknode.pro/TOKEN'");
    console.log("  npx ts-node full_demo.ts");
    console.log();
    console.log("Or:");
    console.log("  npx ts-node full_demo.ts 'https://your-endpoint.hype-mainnet.quiknode.pro/TOKEN'");
    process.exit(1);
  }

  console.log();
  console.log(`Endpoint: ${endpoint.slice(0, 50)}...`);

  try {
    await demoInfoApi(endpoint);
    await demoHypercoreApi(endpoint);
    await demoEvmApi(endpoint);
    await demoWebsocket(endpoint, 5);
    await demoGrpc(endpoint, 5);

    if (privateKey) {
      await demoTrading(endpoint, privateKey);
    } else {
      console.log();
      console.log("--- TRADING (skipped - no PRIVATE_KEY) ---");
    }
  } catch (e) {
    if (e instanceof HyperliquidError) {
      console.log(`\nError: ${e.message}`);
      console.log(`Code: ${e.code}`);
      process.exit(1);
    }
    throw e;
  }

  separator("DONE");
  console.log("All demos completed successfully!");
  console.log();
}

main().catch(console.error);
