#!/usr/bin/env npx ts-node
/**
 * gRPC Streaming Example — High-Performance Real-Time Data
 *
 * Stream trades, orders, L2 book, L4 book, and blocks via gRPC.
 * gRPC provides lower latency than WebSocket for high-frequency trading.
 *
 * gRPC is included with all QuickNode Hyperliquid endpoints — no add-on needed.
 *
 * Setup:
 *     npm install hyperliquid-sdk @grpc/grpc-js @grpc/proto-loader
 *
 * Usage:
 *     export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
 *     npx ts-node stream_grpc.ts
 *
 * The SDK:
 * - Connects to port 10000 automatically
 * - Passes token via x-token header
 * - Handles reconnection with exponential backoff
 * - Manages keepalive pings
 */

import { HyperliquidSDK, GRPCStream, GRPCConnectionState } from 'hyperliquid-sdk';

const ENDPOINT = process.env.ENDPOINT;
if (!ENDPOINT) {
  console.log("gRPC Streaming Example");
  console.log("=".repeat(60));
  console.log();
  console.log("Usage:");
  console.log("  export ENDPOINT='https://YOUR-ENDPOINT.quiknode.pro/TOKEN'");
  console.log("  npx ts-node stream_grpc.ts");
  console.log();
  console.log("gRPC is included with all QuickNode Hyperliquid endpoints.");
  process.exit(1);
}

// Single SDK instance — can use sdk.grpc for streaming
// Note: For standalone usage without SDK, you can also use GRPCStream(ENDPOINT) directly
const sdk = new HyperliquidSDK(ENDPOINT);

function timestamp(): string {
  const now = new Date();
  return now.toTimeString().split(' ')[0] + '.' + String(now.getMilliseconds()).padStart(3, '0');
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXAMPLE 1: Stream Trades
// ═══════════════════════════════════════════════════════════════════════════════

async function streamTradesExample(): Promise<void> {
  console.log("\n" + "=".repeat(60));
  console.log("EXAMPLE 1: Streaming Trades");
  console.log("=".repeat(60));

  let tradeCount = 0;

  const onTrade = (data: Record<string, unknown>) => {
    tradeCount++;
    const coin = data.coin || "?";
    const px = parseFloat(String(data.px || 0));
    const sz = data.sz || "?";
    const side = data.side === "B" ? "BUY " : "SELL";
    console.log(`[${timestamp()}] ${side} ${sz} ${coin} @ $${px.toLocaleString()}`);

    // Stop after 5 trades for demo
    if (tradeCount >= 5) {
      console.log(`\nReceived ${tradeCount} trades. Moving to next example...`);
    }
  };

  // Use standalone GRPCStream for demo (with reconnect=false to stop cleanly)
  // In real usage, you could also use sdk.grpc which shares the endpoint
  const stream = new GRPCStream(ENDPOINT, { reconnect: false });
  stream.trades(["BTC", "ETH"], onTrade);

  console.log("Subscribing to BTC and ETH trades...");
  console.log("-".repeat(60));

  await stream.start();

  // Wait for trades or timeout
  const start = Date.now();
  while (tradeCount < 5 && Date.now() - start < 15000) {
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  stream.stop();
  console.log(`Total trades received: ${tradeCount}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXAMPLE 2: Stream L2 Order Book (Aggregated Price Levels)
// ═══════════════════════════════════════════════════════════════════════════════

async function streamL2BookExample(): Promise<void> {
  console.log("\n" + "=".repeat(60));
  console.log("EXAMPLE 2: Streaming L2 Order Book (Aggregated)");
  console.log("=".repeat(60));
  console.log();
  console.log("L2 book aggregates orders at each price level.");
  console.log("Use nSigFigs to control price aggregation precision.");
  console.log();

  let updateCount = 0;

  const onL2Book = (data: Record<string, unknown>) => {
    updateCount++;

    // L2 book structure: {coin, bids: [[px, sz], ...], asks: [[px, sz], ...]}
    const coin = data.coin || "BTC";
    const bids = (data.bids || []) as unknown[];
    const asks = (data.asks || []) as unknown[];

    if (bids.length && asks.length) {
      const bestBid = bids[0] as string[] || ["N/A", "N/A"];
      const bestAsk = asks[0] as string[] || ["N/A", "N/A"];

      const bidPx = bestBid[0] !== "N/A" ? parseFloat(bestBid[0]) : 0;
      const askPx = bestAsk[0] !== "N/A" ? parseFloat(bestAsk[0]) : 0;
      const spread = bidPx && askPx ? askPx - bidPx : 0;

      console.log(`[${timestamp()}] ${coin} L2 Book:`);
      console.log(`  Best Bid: $${bidPx.toLocaleString()} x ${bestBid[1]}`);
      console.log(`  Best Ask: $${askPx.toLocaleString()} x ${bestAsk[1]}`);
      console.log(`  Spread:   $${spread.toLocaleString()}`);
      console.log(`  Levels:   ${bids.length} bids, ${asks.length} asks`);
      console.log();
    }

    if (updateCount >= 3) {
      console.log("Received 3 L2 updates. Moving to next example...");
    }
  };

  const stream = new GRPCStream(ENDPOINT, { reconnect: false });

  // nSigFigs controls price aggregation:
  // - undefined or 5: Full precision
  // - 4: Aggregate to 4 significant figures
  // - 3: More aggregation (fewer levels, larger sizes)
  stream.l2Book("BTC", onL2Book, { nSigFigs: 5 });

  console.log("Subscribing to BTC L2 order book...");
  console.log("-".repeat(60));

  await stream.start();

  const start = Date.now();
  while (updateCount < 3 && Date.now() - start < 15000) {
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  stream.stop();
  console.log(`Total L2 updates received: ${updateCount}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXAMPLE 3: Stream L4 Order Book (Individual Orders) — CRITICAL FOR TRADING
// ═══════════════════════════════════════════════════════════════════════════════

async function streamL4BookExample(): Promise<void> {
  console.log("\n" + "=".repeat(60));
  console.log("EXAMPLE 3: Streaming L4 Order Book (Individual Orders)");
  console.log("=".repeat(60));
  console.log();
  console.log("L4 book shows EVERY individual order in the book.");
  console.log("This is critical for market making and order flow analysis.");
  console.log();

  let updateCount = 0;

  const onL4Book = (data: Record<string, unknown>) => {
    updateCount++;

    // L4 data has two types: "snapshot" or "diff"
    const updateType = data.type || "unknown";
    const coin = data.coin || "BTC";
    const bids = (data.bids || []) as unknown[];
    const asks = (data.asks || []) as unknown[];

    console.log(`[${timestamp()}] ${coin} L4 Book (${updateType}) #${updateCount}:`);

    if (updateType === "snapshot") {
      // Snapshot: bids/asks are lists of order dicts with limit_px, sz, oid, etc.
      console.log(`  Total: ${bids.length} bids, ${asks.length} asks`);
      console.log("  TOP BIDS:");
      for (let i = 0; i < Math.min(3, bids.length); i++) {
        const bid = bids[i] as Record<string, unknown>;
        if (typeof bid === 'object') {
          const px = bid.limit_px || "?";
          const sz = bid.sz || "?";
          const oid = bid.oid || "?";
          console.log(`    [${i + 1}] $${parseFloat(String(px)).toLocaleString()} x ${sz} (oid: ${oid})`);
        }
      }

      console.log("  TOP ASKS:");
      for (let i = 0; i < Math.min(3, asks.length); i++) {
        const ask = asks[i] as Record<string, unknown>;
        if (typeof ask === 'object') {
          const px = ask.limit_px || "?";
          const sz = ask.sz || "?";
          const oid = ask.oid || "?";
          console.log(`    [${i + 1}] $${parseFloat(String(px)).toLocaleString()} x ${sz} (oid: ${oid})`);
        }
      }
    } else {
      // Diff: contains incremental changes
      const diffData = data.data as Record<string, unknown> | undefined;
      if (diffData) {
        const keys = Object.keys(diffData).slice(0, 5);
        console.log(`  Changes: ${JSON.stringify(keys)}...`);
      } else {
        console.log("  (incremental update)");
      }
    }

    console.log();

    if (updateCount >= 3) {
      console.log("Received 3 L4 updates. Moving to next example...");
    }
  };

  const stream = new GRPCStream(ENDPOINT, { reconnect: false });
  stream.l4Book("BTC", onL4Book);

  console.log("Subscribing to BTC L4 order book (individual orders)...");
  console.log("-".repeat(60));

  await stream.start();

  const start = Date.now();
  while (updateCount < 3 && Date.now() - start < 15000) {
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  stream.stop();
  console.log(`Total L4 updates received: ${updateCount}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXAMPLE 4: Stream Orders (Order Lifecycle Events)
// ═══════════════════════════════════════════════════════════════════════════════

async function streamOrdersExample(): Promise<void> {
  console.log("\n" + "=".repeat(60));
  console.log("EXAMPLE 4: Streaming Order Events");
  console.log("=".repeat(60));
  console.log();
  console.log("Order events: open, filled, partially_filled, canceled, triggered");
  console.log();

  let orderCount = 0;

  const onOrder = (data: Record<string, unknown>) => {
    orderCount++;

    const coin = data.coin || "?";
    const status = data.status || "?";
    const side = data.side === "B" ? "BUY " : "SELL";
    const px = data.px || "?";
    const sz = data.sz || "?";
    const oid = data.oid || "?";

    console.log(`[${timestamp()}] ORDER ${String(status).toUpperCase()}: ${side} ${sz} ${coin} @ ${px} (oid: ${oid})`);

    if (orderCount >= 5) {
      console.log(`\nReceived ${orderCount} order events. Moving to next example...`);
    }
  };

  const stream = new GRPCStream(ENDPOINT, { reconnect: false });

  // Can filter by specific users (optional)
  // stream.orders(["BTC", "ETH"], onOrder, { users: ["0x..."] });
  stream.orders(["BTC", "ETH"], onOrder);

  console.log("Subscribing to BTC and ETH order events...");
  console.log("-".repeat(60));

  await stream.start();

  const start = Date.now();
  while (orderCount < 5 && Date.now() - start < 15000) {
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  stream.stop();
  console.log(`Total order events received: ${orderCount}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXAMPLE 5: Stream Blocks
// ═══════════════════════════════════════════════════════════════════════════════

async function streamBlocksExample(): Promise<void> {
  console.log("\n" + "=".repeat(60));
  console.log("EXAMPLE 5: Streaming Blocks");
  console.log("=".repeat(60));

  let blockCount = 0;

  const onBlock = (data: Record<string, unknown>) => {
    blockCount++;

    // Block structure: {"abci_block": {"time": "...", "signed_action_bundles": [...]}, "resps": [...]}
    const abciBlock = (data.abci_block || {}) as Record<string, unknown>;
    const blockTime = abciBlock.time || "?";
    const bundles = ((abciBlock.signed_action_bundles || []) as unknown[]).length;

    console.log(`[${timestamp()}] BLOCK @ ${blockTime} (${bundles} bundles)`);

    if (blockCount >= 3) {
      console.log(`\nReceived ${blockCount} blocks. Demo complete!`);
    }
  };

  const stream = new GRPCStream(ENDPOINT, { reconnect: false });
  stream.blocks(onBlock);

  console.log("Subscribing to blocks...");
  console.log("-".repeat(60));

  await stream.start();

  const start = Date.now();
  while (blockCount < 3 && Date.now() - start < 30000) {
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  stream.stop();
  console.log(`Total blocks received: ${blockCount}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXAMPLE 6: Multiple Subscriptions with Connection Management
// ═══════════════════════════════════════════════════════════════════════════════

async function multiStreamExample(): Promise<void> {
  console.log("\n" + "=".repeat(60));
  console.log("EXAMPLE 6: Multiple Subscriptions + Connection Management");
  console.log("=".repeat(60));

  const counts = { trades: 0, l2: 0, orders: 0 };

  const onTrade = (data: Record<string, unknown>) => {
    counts.trades++;
    const coin = data.coin || "?";
    console.log(`[TRADE] ${coin} - Total: ${counts.trades}`);
  };

  const onL2 = (data: Record<string, unknown>) => {
    counts.l2++;
    const coin = data.coin || "?";
    console.log(`[L2]    ${coin} - Total: ${counts.l2}`);
  };

  const onOrder = (data: Record<string, unknown>) => {
    counts.orders++;
    const status = data.status || "?";
    console.log(`[ORDER] ${status} - Total: ${counts.orders}`);
  };

  const onState = (state: GRPCConnectionState) => {
    console.log(`[STATE] ${state}`);
  };

  const onConnect = () => {
    console.log("[CONNECTED] All streams active");
  };

  const onError = (error: unknown) => {
    console.log(`[ERROR] ${error}`);
  };

  const stream = new GRPCStream(ENDPOINT, {
    onError,
    onConnect,
    onStateChange: onState,
    reconnect: true,
    maxReconnectAttempts: 3,
  });

  // Chain multiple subscriptions
  stream.trades(["BTC"], onTrade);
  stream.l2Book("ETH", onL2);
  stream.orders(["BTC", "ETH"], onOrder);

  console.log("Subscribing to BTC trades, ETH L2 book, BTC/ETH orders...");
  console.log("-".repeat(60));

  // Handle Ctrl+C
  process.on('SIGINT', () => {
    console.log("\nStopping...");
    stream.stop();
    process.exit(0);
  });

  await stream.start();

  // Run for 20 seconds
  await new Promise(resolve => setTimeout(resolve, 20000));

  stream.stop();

  console.log();
  console.log("=".repeat(60));
  console.log("SUMMARY");
  console.log("=".repeat(60));
  console.log(`  Trades received: ${counts.trades}`);
  console.log(`  L2 updates:      ${counts.l2}`);
  console.log(`  Order events:    ${counts.orders}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// MAIN
// ═══════════════════════════════════════════════════════════════════════════════

async function main() {
  console.log("=".repeat(60));
  console.log("gRPC Streaming Examples");
  console.log("=".repeat(60));
  console.log(`Endpoint: ${ENDPOINT.slice(0, 50)}...`);
  console.log();
  console.log("This demo shows all gRPC streaming capabilities:");
  console.log("  1. Trades — Real-time executed trades");
  console.log("  2. L2 Book — Aggregated order book by price level");
  console.log("  3. L4 Book — Individual orders (CRITICAL for trading)");
  console.log("  4. Orders — Order lifecycle events");
  console.log("  5. Blocks — Block data");
  console.log("  6. Multi-stream — Multiple subscriptions + management");
  console.log();

  // Run examples
  try {
    await streamTradesExample();
    await streamL2BookExample();
    await streamL4BookExample();
    await streamOrdersExample();
    await streamBlocksExample();
    // await multiStreamExample();  // Uncomment for full demo

    console.log();
    console.log("=".repeat(60));
    console.log("All examples completed!");
    console.log("=".repeat(60));

  } catch (e) {
    if (e instanceof Error && e.message.includes('interrupt')) {
      console.log("\nDemo interrupted.");
    } else {
      console.log(`\nError: ${e}`);
      throw e;
    }
  }
}

main().catch(console.error);
