#!/usr/bin/env npx ts-node
/**
 * Order Book Streaming Example — L2 and L4 Order Books via gRPC
 *
 * This example demonstrates how to stream order book data via gRPC:
 * - L2 Book: Aggregated by price level (total size and order count per price)
 * - L4 Book: Individual orders with order IDs
 *
 * Note: L2/L4 order books are only available via gRPC on QuickNode.
 *       WebSocket streaming provides book_updates (incremental deltas) instead.
 *
 * Use cases:
 * - L2 Book: Market depth, spread monitoring, analytics dashboards
 * - L4 Book: HFT, quant trading, market making, order flow analysis
 *
 * Setup:
 *     npm install hyperliquid-sdk @grpc/grpc-js @grpc/proto-loader
 *
 * Usage:
 *     export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
 *     npx ts-node stream_orderbook.ts
 */

import { GRPCStream } from 'hyperliquid-sdk';

const ENDPOINT = process.env.ENDPOINT;
if (!ENDPOINT) {
  console.log("Order Book Streaming Example");
  console.log("=".repeat(60));
  console.log();
  console.log("Usage:");
  console.log("  export ENDPOINT='https://YOUR-ENDPOINT.quiknode.pro/TOKEN'");
  console.log("  npx ts-node stream_orderbook.ts");
  process.exit(1);
}

function timestamp(): string {
  const now = new Date();
  return now.toTimeString().split(' ')[0] + '.' + String(now.getMilliseconds()).padStart(3, '0');
}

// ═══════════════════════════════════════════════════════════════════════════════
// L2 ORDER BOOK (Aggregated Price Levels)
// ═══════════════════════════════════════════════════════════════════════════════

class L2BookTracker {
  coin: string;
  bids: unknown[] = [];
  asks: unknown[] = [];
  lastUpdate = 0;

  constructor(coin: string) {
    this.coin = coin;
  }

  update(data: Record<string, unknown>): void {
    this.bids = (data.bids || []) as unknown[];
    this.asks = (data.asks || []) as unknown[];
    this.lastUpdate = Date.now();
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

  depth(levels: number = 5): Record<string, number> {
    let bidDepth = 0;
    for (const level of this.bids.slice(0, levels)) {
      if (Array.isArray(level) && level.length >= 2) {
        bidDepth += parseFloat(String(level[1]));
      } else if (typeof level === 'object' && level !== null) {
        bidDepth += parseFloat(String((level as Record<string, unknown>).sz || 0));
      }
    }

    let askDepth = 0;
    for (const level of this.asks.slice(0, levels)) {
      if (Array.isArray(level) && level.length >= 2) {
        askDepth += parseFloat(String(level[1]));
      } else if (typeof level === 'object' && level !== null) {
        askDepth += parseFloat(String((level as Record<string, unknown>).sz || 0));
      }
    }

    return { bidDepth, askDepth };
  }

  display(): void {
    const [bidPx, bidSz] = this.bestBid();
    const [askPx, askSz] = this.bestAsk();
    const d = this.depth();

    console.log(`\n${this.coin} L2 Order Book`);
    console.log("-".repeat(40));
    console.log(`  Best Bid:   $${bidPx.toLocaleString().padStart(12)} x ${bidSz.toFixed(4).padStart(10)}`);
    console.log(`  Best Ask:   $${askPx.toLocaleString().padStart(12)} x ${askSz.toFixed(4).padStart(10)}`);
    console.log(`  Spread:     $${this.spread().toLocaleString().padStart(12)} (${this.spreadBps().toFixed(2)} bps)`);
    console.log(`  Bid Depth:  ${d.bidDepth.toFixed(4).padStart(23)} (top 5)`);
    console.log(`  Ask Depth:  ${d.askDepth.toFixed(4).padStart(23)} (top 5)`);
    console.log(`  Levels:     ${this.bids.length} bids, ${this.asks.length} asks`);
  }
}

async function streamL2Grpc(): Promise<void> {
  console.log("\n" + "=".repeat(60));
  console.log("L2 ORDER BOOK via gRPC");
  console.log("=".repeat(60));
  console.log();
  console.log("L2 book aggregates all orders at each price level.");
  console.log("nSigFigs controls aggregation precision.");
  console.log();

  const tracker = new L2BookTracker("BTC");
  let updateCount = 0;

  const onL2 = (data: Record<string, unknown>) => {
    updateCount++;
    tracker.update(data);

    if (updateCount <= 3) {
      tracker.display();
    }
  };

  const stream = new GRPCStream(ENDPOINT, { reconnect: false });

  // nSigFigs options:
  // - 5: Full precision (most levels)
  // - 4: Some aggregation
  // - 3: More aggregation (fewer levels, larger sizes)
  stream.l2Book("BTC", onL2, { nSigFigs: 5 });

  console.log("Subscribing to BTC L2 book via gRPC...");
  console.log("-".repeat(60));

  await stream.start();

  const start = Date.now();
  while (updateCount < 3 && Date.now() - start < 15000) {
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  stream.stop();
  console.log(`\nReceived ${updateCount} L2 updates via gRPC`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// L4 ORDER BOOK (Individual Orders) — CRITICAL FOR TRADING
// ═══════════════════════════════════════════════════════════════════════════════

interface OrderEntry {
  px: string;
  sz: string;
  oid: string;
  side: string;
}

class L4BookTracker {
  coin: string;
  bids: Map<string, OrderEntry> = new Map();
  asks: Map<string, OrderEntry> = new Map();
  lastUpdate = 0;

  constructor(coin: string) {
    this.coin = coin;
  }

  update(data: Record<string, unknown>): void {
    this.lastUpdate = Date.now();

    // Process bids
    for (const bid of (data.bids || []) as unknown[]) {
      this.processLevel(bid, this.bids, "bid");
    }

    // Process asks
    for (const ask of (data.asks || []) as unknown[]) {
      this.processLevel(ask, this.asks, "ask");
    }
  }

  private processLevel(level: unknown, book: Map<string, OrderEntry>, side: string): void {
    if (Array.isArray(level)) {
      if (level.length >= 3) {
        // Format: [price, size, order_id]
        const px = String(level[0]);
        const sz = String(level[1]);
        const oid = String(level[2]);
        if (parseFloat(sz) === 0) {
          book.delete(oid);
        } else {
          book.set(oid, { px, sz, oid, side });
        }
      } else if (level.length >= 2 && Array.isArray(level[1])) {
        // Format: [price, [[size, oid], ...]]
        const px = String(level[0]);
        for (const order of level[1]) {
          if (Array.isArray(order) && order.length >= 2) {
            const sz = String(order[0]);
            const oid = String(order[1]);
            if (parseFloat(sz) === 0) {
              book.delete(oid);
            } else {
              book.set(oid, { px, sz, oid, side });
            }
          }
        }
      }
    }
  }

  getSortedBids(): OrderEntry[] {
    return Array.from(this.bids.values()).sort(
      (a, b) => parseFloat(b.px) - parseFloat(a.px)
    );
  }

  getSortedAsks(): OrderEntry[] {
    return Array.from(this.asks.values()).sort(
      (a, b) => parseFloat(a.px) - parseFloat(b.px)
    );
  }

  totalOrders(): [number, number] {
    return [this.bids.size, this.asks.size];
  }

  display(levels: number = 5): void {
    const sortedBids = this.getSortedBids();
    const sortedAsks = this.getSortedAsks();

    console.log(`\n${this.coin} L4 Order Book (Individual Orders)`);
    console.log("=".repeat(60));

    // Group orders by price
    const bidPrices: Map<number, OrderEntry[]> = new Map();
    for (const bid of sortedBids.slice(0, 20)) {
      const px = parseFloat(bid.px);
      if (!bidPrices.has(px)) bidPrices.set(px, []);
      bidPrices.get(px)!.push(bid);
    }

    const askPrices: Map<number, OrderEntry[]> = new Map();
    for (const ask of sortedAsks.slice(0, 20)) {
      const px = parseFloat(ask.px);
      if (!askPrices.has(px)) askPrices.set(px, []);
      askPrices.get(px)!.push(ask);
    }

    // Display asks (top levels, reversed for display)
    console.log("\nASKS (top 5 price levels):");
    const sortedAskPrices = Array.from(askPrices.keys()).sort((a, b) => a - b).slice(0, levels);
    for (const px of sortedAskPrices.reverse()) {
      const orders = askPrices.get(px)!;
      const totalSz = orders.reduce((sum, o) => sum + parseFloat(o.sz), 0);
      console.log(`  $${px.toLocaleString().padStart(12)} | ${totalSz.toFixed(4).padStart(10)} | ${orders.length.toString().padStart(3)} orders`);
      // Show individual orders (first 3)
      for (const order of orders.slice(0, 3)) {
        console.log(`               └─ ${parseFloat(order.sz).toFixed(4).padStart(10)} (oid: ${order.oid.slice(0, 8)}...)`);
      }
    }

    console.log("  " + "-".repeat(56));
    console.log("  " + " ".repeat(14) + "SPREAD");
    console.log("  " + "-".repeat(56));

    // Display bids (top levels)
    console.log("\nBIDS (top 5 price levels):");
    const sortedBidPrices = Array.from(bidPrices.keys()).sort((a, b) => b - a).slice(0, levels);
    for (const px of sortedBidPrices) {
      const orders = bidPrices.get(px)!;
      const totalSz = orders.reduce((sum, o) => sum + parseFloat(o.sz), 0);
      console.log(`  $${px.toLocaleString().padStart(12)} | ${totalSz.toFixed(4).padStart(10)} | ${orders.length.toString().padStart(3)} orders`);
      for (const order of orders.slice(0, 3)) {
        console.log(`               └─ ${parseFloat(order.sz).toFixed(4).padStart(10)} (oid: ${order.oid.slice(0, 8)}...)`);
      }
    }

    const [bidCount, askCount] = this.totalOrders();
    console.log(`\nTotal: ${bidCount} bid orders, ${askCount} ask orders`);
  }
}

async function streamL4Book(): Promise<void> {
  console.log("\n" + "=".repeat(60));
  console.log("L4 ORDER BOOK via gRPC (Individual Orders)");
  console.log("=".repeat(60));
  console.log();
  console.log("L4 book shows EVERY individual order with order ID.");
  console.log("This is CRITICAL for market making and order flow analysis.");
  console.log();
  console.log("Use cases:");
  console.log("  - See exact queue position");
  console.log("  - Detect large orders / icebergs");
  console.log("  - Know exactly what you're crossing");
  console.log("  - Analyze order flow");
  console.log();

  const tracker = new L4BookTracker("BTC");
  let updateCount = 0;

  const onL4 = (data: Record<string, unknown>) => {
    updateCount++;
    tracker.update(data);

    if (updateCount <= 3) {
      tracker.display(3);
      console.log();
    }
  };

  const stream = new GRPCStream(ENDPOINT, { reconnect: false });
  stream.l4Book("BTC", onL4);

  console.log("Subscribing to BTC L4 book via gRPC...");
  console.log("-".repeat(60));

  await stream.start();

  const start = Date.now();
  while (updateCount < 3 && Date.now() - start < 15000) {
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  stream.stop();
  console.log(`\nReceived ${updateCount} L4 updates`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// COMPARISON: L2 vs L4 Order Book
// ═══════════════════════════════════════════════════════════════════════════════

function comparison(): void {
  console.log("\n" + "=".repeat(60));
  console.log("L2 vs L4 ORDER BOOK COMPARISON");
  console.log("=".repeat(60));
  console.log();
  console.log("┌─────────────────────────────────────────────────────────────┐");
  console.log("│                    L2 ORDER BOOK                            │");
  console.log("├─────────────────────────────────────────────────────────────┤");
  console.log("│ • Aggregated by price level                                 │");
  console.log("│ • Shows total size at each price                            │");
  console.log("│ • Available via gRPC (StreamL2Book)                         │");
  console.log("│ • Lower bandwidth                                           │");
  console.log("│ • Good for: Price monitoring, simple trading                │");
  console.log("├─────────────────────────────────────────────────────────────┤");
  console.log("│ Example:                                                    │");
  console.log("│   Price: $95,000.00 | Total Size: 10.5 BTC                  │");
  console.log("│   (You don't know how many orders or their sizes)           │");
  console.log("└─────────────────────────────────────────────────────────────┘");
  console.log();
  console.log("┌─────────────────────────────────────────────────────────────┐");
  console.log("│                    L4 ORDER BOOK                            │");
  console.log("├─────────────────────────────────────────────────────────────┤");
  console.log("│ • Individual orders with order IDs                          │");
  console.log("│ • Shows each order separately                               │");
  console.log("│ • Available via gRPC (StreamL4Book)                         │");
  console.log("│ • Higher bandwidth but more detail                          │");
  console.log("│ • Good for: Market making, HFT, order flow analysis         │");
  console.log("├─────────────────────────────────────────────────────────────┤");
  console.log("│ Example:                                                    │");
  console.log("│   Price: $95,000.00                                         │");
  console.log("│     └─ Order 1: 5.0 BTC (oid: abc123...)                    │");
  console.log("│     └─ Order 2: 3.0 BTC (oid: def456...)                    │");
  console.log("│     └─ Order 3: 2.5 BTC (oid: ghi789...)                    │");
  console.log("│   (You see every order and can track queue position)        │");
  console.log("└─────────────────────────────────────────────────────────────┘");
  console.log();
  console.log("Note: For incremental book changes (deltas), use WebSocket:");
  console.log("  stream.bookUpdates(coins, callback)");
  console.log();
}

// ═══════════════════════════════════════════════════════════════════════════════
// MAIN
// ═══════════════════════════════════════════════════════════════════════════════

async function main() {
  console.log("=".repeat(60));
  console.log("Order Book Streaming Examples (gRPC)");
  console.log("=".repeat(60));
  console.log(`Endpoint: ${ENDPOINT.slice(0, 50)}...`);

  try {
    // Show comparison
    comparison();

    // Run L2 example
    await streamL2Grpc();

    // Run L4 example (CRITICAL)
    await streamL4Book();

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
