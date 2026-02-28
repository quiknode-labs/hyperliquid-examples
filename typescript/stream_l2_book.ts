#!/usr/bin/env npx ts-node
/**
 * L2 Order Book Streaming — Aggregated Price Levels
 *
 * L2 order book shows total size at each price level (aggregated).
 * Available via both WebSocket and gRPC.
 *
 * Use L2 for:
 * - Price monitoring
 * - Basic trading strategies
 * - Lower bandwidth requirements
 *
 * Use L4 (gRPC only) when you need:
 * - Individual order IDs
 * - Queue position tracking
 * - Order flow analysis
 *
 * Setup:
 *     npm install hyperliquid-sdk @grpc/grpc-js @grpc/proto-loader
 *
 * Usage:
 *     export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
 *     npx ts-node stream_l2_book.ts
 */

import { GRPCStream, Stream } from 'hyperliquid-sdk';

const ENDPOINT = process.env.ENDPOINT;
if (!ENDPOINT) {
  console.log("L2 Order Book Streaming Example");
  console.log("=".repeat(60));
  console.log();
  console.log("Usage:");
  console.log("  export ENDPOINT='https://YOUR-ENDPOINT.quiknode.pro/TOKEN'");
  console.log("  npx ts-node stream_l2_book.ts");
  process.exit(1);
}

function timestamp(): string {
  const now = new Date();
  return now.toTimeString().split(' ')[0] + '.' + String(now.getMilliseconds()).padStart(3, '0');
}

class L2BookTracker {
  coin: string;
  source: string;
  bids: unknown[] = [];
  asks: unknown[] = [];
  updateCount = 0;

  constructor(coin: string, source: string = "grpc") {
    this.coin = coin;
    this.source = source;
  }

  updateFromGrpc(data: Record<string, unknown>): void {
    this.updateCount++;
    this.bids = (data.bids || []) as unknown[];
    this.asks = (data.asks || []) as unknown[];
  }

  updateFromWebsocket(data: Record<string, unknown>): void {
    this.updateCount++;
    const book = (data.data || {}) as Record<string, unknown>;
    const levels = (book.levels || [[], []]) as unknown[][];
    this.bids = levels[0] || [];
    this.asks = levels[1] || [];
  }

  bestBid(): [number, number] {
    if (!this.bids.length) return [0, 0];
    const bid = this.bids[0];
    if (Array.isArray(bid)) return [parseFloat(String(bid[0])), parseFloat(String(bid[1]))];
    const b = bid as Record<string, unknown>;
    return [parseFloat(String(b.px || 0)), parseFloat(String(b.sz || 0))];
  }

  bestAsk(): [number, number] {
    if (!this.asks.length) return [0, 0];
    const ask = this.asks[0];
    if (Array.isArray(ask)) return [parseFloat(String(ask[0])), parseFloat(String(ask[1]))];
    const a = ask as Record<string, unknown>;
    return [parseFloat(String(a.px || 0)), parseFloat(String(a.sz || 0))];
  }

  spread(): number {
    const [bidPx] = this.bestBid();
    const [askPx] = this.bestAsk();
    return bidPx && askPx ? askPx - bidPx : 0;
  }

  spreadBps(): number {
    const [bidPx] = this.bestBid();
    const [askPx] = this.bestAsk();
    if (!bidPx || !askPx) return 0;
    const mid = (bidPx + askPx) / 2;
    return (askPx - bidPx) / mid * 10000;
  }

  display(levels: number = 5): void {
    const [bidPx, bidSz] = this.bestBid();
    const [askPx, askSz] = this.bestAsk();

    console.log(`\n[${timestamp()}] ${this.coin} L2 Book (${this.source.toUpperCase()}) #${this.updateCount}`);
    console.log("-".repeat(50));

    // Show top ask levels (reversed)
    console.log(" ASKS:");
    const askSlice = this.asks.slice(0, levels).reverse();
    for (const ask of askSlice) {
      let px: number, sz: number;
      if (Array.isArray(ask)) {
        px = parseFloat(String(ask[0]));
        sz = parseFloat(String(ask[1]));
      } else {
        const a = ask as Record<string, unknown>;
        px = parseFloat(String(a.px || 0));
        sz = parseFloat(String(a.sz || 0));
      }
      console.log(`    $${px.toLocaleString().padStart(12)} │ ${sz.toFixed(4).padStart(10)}`);
    }

    console.log(`  ${"─".repeat(30)}`);
    console.log(`  SPREAD: $${this.spread().toLocaleString()} (${this.spreadBps().toFixed(1)} bps)`);
    console.log(`  ${"─".repeat(30)}`);

    // Show top bid levels
    console.log(" BIDS:");
    for (const bid of this.bids.slice(0, levels)) {
      let px: number, sz: number;
      if (Array.isArray(bid)) {
        px = parseFloat(String(bid[0]));
        sz = parseFloat(String(bid[1]));
      } else {
        const b = bid as Record<string, unknown>;
        px = parseFloat(String(b.px || 0));
        sz = parseFloat(String(b.sz || 0));
      }
      console.log(`    $${px.toLocaleString().padStart(12)} │ ${sz.toFixed(4).padStart(10)}`);
    }

    console.log(`\n  Levels: ${this.bids.length} bids, ${this.asks.length} asks`);
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// gRPC L2 BOOK
// ═══════════════════════════════════════════════════════════════════════════════

async function streamL2Grpc(): Promise<void> {
  console.log("\n" + "=".repeat(60));
  console.log("L2 ORDER BOOK via gRPC");
  console.log("=".repeat(60));
  console.log();
  console.log("gRPC provides lower latency than WebSocket.");
  console.log("nSigFigs controls price aggregation (3-5).");
  console.log();

  const book = new L2BookTracker("BTC", "grpc");

  const onL2 = (data: Record<string, unknown>) => {
    book.updateFromGrpc(data);
    if (book.updateCount <= 5) {
      book.display(3);
    }
  };

  const onConnect = () => {
    console.log(`[${timestamp()}] gRPC connected`);
  };

  const stream = new GRPCStream(ENDPOINT, { onConnect, reconnect: false });

  // nSigFigs options:
  // 5 = full precision (most levels)
  // 4 = some aggregation
  // 3 = more aggregation (fewer levels, larger sizes)
  stream.l2Book("BTC", onL2, { nSigFigs: 5 });

  console.log("Subscribing to BTC L2 book via gRPC (nSigFigs=5)...");
  console.log("-".repeat(60));

  await stream.start();

  const start = Date.now();
  while (book.updateCount < 5 && Date.now() - start < 15000) {
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  stream.stop();
  console.log(`\nReceived ${book.updateCount} L2 updates via gRPC`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// WebSocket L2 BOOK
// ═══════════════════════════════════════════════════════════════════════════════

async function streamL2Websocket(): Promise<void> {
  console.log("\n" + "=".repeat(60));
  console.log("L2 ORDER BOOK via WebSocket");
  console.log("=".repeat(60));

  const book = new L2BookTracker("BTC", "websocket");

  const onL2 = (data: Record<string, unknown>) => {
    book.updateFromWebsocket(data);
    if (book.updateCount <= 5) {
      book.display(3);
    }
  };

  const onOpen = () => {
    console.log(`[${timestamp()}] WebSocket connected`);
  };

  const stream = new Stream(ENDPOINT, { onOpen, reconnect: false });
  stream.l2Book("BTC", onL2);

  console.log("Subscribing to BTC L2 book via WebSocket...");
  console.log("-".repeat(60));

  await stream.start();

  const start = Date.now();
  while (book.updateCount < 5 && Date.now() - start < 15000) {
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  stream.stop();
  console.log(`\nReceived ${book.updateCount} L2 updates via WebSocket`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// COMPARE L2 SOURCES
// ═══════════════════════════════════════════════════════════════════════════════

function compareSources(): void {
  console.log("\n" + "=".repeat(60));
  console.log("COMPARISON: gRPC vs WebSocket");
  console.log("=".repeat(60));
  console.log();
  console.log("┌─────────────────────────────────────────────────────────────┐");
  console.log("│                      L2 VIA gRPC                            │");
  console.log("├─────────────────────────────────────────────────────────────┤");
  console.log("│ • Lower latency                                             │");
  console.log("│ • nSigFigs parameter for aggregation control                │");
  console.log("│ • Best for: HFT, latency-sensitive apps                     │");
  console.log("│ • Port: 10000                                               │");
  console.log("└─────────────────────────────────────────────────────────────┘");
  console.log();
  console.log("┌─────────────────────────────────────────────────────────────┐");
  console.log("│                    L2 VIA WebSocket                         │");
  console.log("├─────────────────────────────────────────────────────────────┤");
  console.log("│ • Standard WebSocket (443)                                  │");
  console.log("│ • Works in browsers                                         │");
  console.log("│ • More subscription types available                         │");
  console.log("│ • Best for: Web apps, general use                           │");
  console.log("└─────────────────────────────────────────────────────────────┘");
  console.log();
}

// ═══════════════════════════════════════════════════════════════════════════════
// MAIN
// ═══════════════════════════════════════════════════════════════════════════════

async function main() {
  console.log("=".repeat(60));
  console.log("L2 ORDER BOOK STREAMING");
  console.log("=".repeat(60));
  console.log(`Endpoint: ${ENDPOINT.slice(0, 50)}...`);

  try {
    // Show comparison
    compareSources();

    // Stream via gRPC
    await streamL2Grpc();

    // Stream via WebSocket
    await streamL2Websocket();

    console.log();
    console.log("=".repeat(60));
    console.log("All L2 examples completed!");
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
