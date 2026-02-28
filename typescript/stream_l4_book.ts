#!/usr/bin/env npx ts-node
/**
 * L4 Order Book Streaming via gRPC — Individual Orders with Order IDs
 *
 * L4 order book is CRITICAL for:
 * - Market making: Know your exact queue position
 * - Order flow analysis: Detect large orders, icebergs
 * - Optimal execution: See exactly what you're crossing
 * - HFT: Lower latency than WebSocket
 *
 * This example shows how to:
 * 1. Stream L4 order book updates
 * 2. Track individual orders
 * 3. Calculate depth and queue position
 *
 * Setup:
 *     npm install hyperliquid-sdk @grpc/grpc-js @grpc/proto-loader
 *
 * Usage:
 *     export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
 *     npx ts-node stream_l4_book.ts
 */

import { GRPCStream, GRPCConnectionState } from 'hyperliquid-sdk';

const ENDPOINT = process.env.ENDPOINT;
if (!ENDPOINT) {
  console.log("L4 Order Book Streaming Example");
  console.log("=".repeat(60));
  console.log();
  console.log("L4 book shows EVERY individual order with order IDs.");
  console.log("This is essential for market making and order flow analysis.");
  console.log();
  console.log("Usage:");
  console.log("  export ENDPOINT='https://YOUR-ENDPOINT.quiknode.pro/TOKEN'");
  console.log("  npx ts-node stream_l4_book.ts");
  process.exit(1);
}

function timestamp(): string {
  const now = new Date();
  return now.toTimeString().split(' ')[0] + '.' + String(now.getMilliseconds()).padStart(3, '0');
}

interface OrderEntry {
  px: string;
  sz: string;
  oid: string;
  side: string;
  time: number;
}

class L4BookManager {
  /**
   * Manage L4 order book state.
   *
   * L4 book tracks individual orders with their order IDs,
   * allowing you to:
   * - Know exact queue position at each price level
   * - Track specific orders (your own or large orders)
   * - Calculate precise depth
   */

  coin: string;
  bids: Map<string, OrderEntry> = new Map();
  asks: Map<string, OrderEntry> = new Map();
  updateCount = 0;
  lastUpdate = 0;

  constructor(coin: string) {
    this.coin = coin;
  }

  processUpdate(data: Record<string, unknown>): void {
    this.updateCount++;
    this.lastUpdate = Date.now();

    // Process bids
    for (const level of (data.bids || []) as unknown[]) {
      this.processLevel(level, this.bids, "bid");
    }

    // Process asks
    for (const level of (data.asks || []) as unknown[]) {
      this.processLevel(level, this.asks, "ask");
    }
  }

  private processLevel(level: unknown, book: Map<string, OrderEntry>, side: string): void {
    if (!Array.isArray(level)) return;

    // Format 1: [price, size, order_id]
    if (level.length >= 3 && !Array.isArray(level[1])) {
      const px = String(level[0]);
      const sz = String(level[1]);
      const oid = String(level[2]);
      if (parseFloat(sz) === 0) {
        // Order removed
        book.delete(oid);
      } else {
        // Order added or updated
        book.set(oid, { px, sz, oid, side, time: Date.now() });
      }
    }

    // Format 2: [price, [[size, oid], ...]]
    else if (level.length >= 2 && Array.isArray(level[1])) {
      const px = String(level[0]);
      for (const order of level[1]) {
        if (Array.isArray(order) && order.length >= 2) {
          const sz = String(order[0]);
          const oid = String(order[1]);
          if (parseFloat(sz) === 0) {
            book.delete(oid);
          } else {
            book.set(oid, { px, sz, oid, side, time: Date.now() });
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

  getBestBid(): OrderEntry | undefined {
    const sorted = this.getSortedBids();
    return sorted[0];
  }

  getBestAsk(): OrderEntry | undefined {
    const sorted = this.getSortedAsks();
    return sorted[0];
  }

  getSpread(): number {
    const bestBid = this.getBestBid();
    const bestAsk = this.getBestAsk();
    if (bestBid && bestAsk) {
      return parseFloat(bestAsk.px) - parseFloat(bestBid.px);
    }
    return 0;
  }

  getOrdersAtPrice(price: number, side: string = "bid"): OrderEntry[] {
    const book = side === "bid" ? this.bids : this.asks;
    return Array.from(book.values()).filter(
      order => Math.abs(parseFloat(order.px) - price) < 0.01
    );
  }

  getQueuePosition(orderId: string): number {
    /**
     * Get queue position for an order.
     * Returns position (1 = first in queue) or 0 if not found.
     */
    // Check bids
    for (const order of this.bids.values()) {
      if (order.oid === orderId) {
        const price = parseFloat(order.px);
        const ordersAtPrice = this.getOrdersAtPrice(price, "bid");
        // Sort by time (earlier = better position)
        const sorted = ordersAtPrice.sort((a, b) => a.time - b.time);
        for (let i = 0; i < sorted.length; i++) {
          if (sorted[i].oid === orderId) {
            return i + 1;
          }
        }
        return 0;
      }
    }

    // Check asks
    for (const order of this.asks.values()) {
      if (order.oid === orderId) {
        const price = parseFloat(order.px);
        const ordersAtPrice = this.getOrdersAtPrice(price, "ask");
        const sorted = ordersAtPrice.sort((a, b) => a.time - b.time);
        for (let i = 0; i < sorted.length; i++) {
          if (sorted[i].oid === orderId) {
            return i + 1;
          }
        }
        return 0;
      }
    }

    return 0;
  }

  getDepthAtLevels(levels: number = 5): Record<string, number | number> {
    const sortedBids = this.getSortedBids();
    const sortedAsks = this.getSortedAsks();

    // Group by price
    const bidByPrice: Map<number, number> = new Map();
    for (const order of sortedBids) {
      const px = parseFloat(order.px);
      bidByPrice.set(px, (bidByPrice.get(px) || 0) + parseFloat(order.sz));
    }

    const askByPrice: Map<number, number> = new Map();
    for (const order of sortedAsks) {
      const px = parseFloat(order.px);
      askByPrice.set(px, (askByPrice.get(px) || 0) + parseFloat(order.sz));
    }

    // Get top N levels
    const bidPrices = Array.from(bidByPrice.keys()).sort((a, b) => b - a).slice(0, levels);
    const askPrices = Array.from(askByPrice.keys()).sort((a, b) => a - b).slice(0, levels);

    let bidDepth = 0;
    for (const p of bidPrices) bidDepth += bidByPrice.get(p) || 0;

    let askDepth = 0;
    for (const p of askPrices) askDepth += askByPrice.get(p) || 0;

    return {
      bidDepth,
      askDepth,
      bidLevels: bidPrices.length,
      askLevels: askPrices.length,
      bidOrders: this.bids.size,
      askOrders: this.asks.size,
    };
  }

  display(levels: number = 3): void {
    const sortedBids = this.getSortedBids();
    const sortedAsks = this.getSortedAsks();
    const depth = this.getDepthAtLevels(levels);

    console.log(`\n${"=".repeat(60)}`);
    console.log(`${this.coin} L4 ORDER BOOK (Update #${this.updateCount})`);
    console.log("=".repeat(60));

    // Group orders by price for display
    const askByPrice: Map<number, OrderEntry[]> = new Map();
    for (const order of sortedAsks.slice(0, 20)) {
      const px = parseFloat(order.px);
      if (!askByPrice.has(px)) askByPrice.set(px, []);
      askByPrice.get(px)!.push(order);
    }

    const bidByPrice: Map<number, OrderEntry[]> = new Map();
    for (const order of sortedBids.slice(0, 20)) {
      const px = parseFloat(order.px);
      if (!bidByPrice.has(px)) bidByPrice.set(px, []);
      bidByPrice.get(px)!.push(order);
    }

    // Display asks (reversed so best ask is near spread)
    console.log("\n ASKS:");
    const askPrices = Array.from(askByPrice.keys()).sort((a, b) => a - b).slice(0, levels);
    for (const px of askPrices.reverse()) {
      const orders = askByPrice.get(px)!;
      const totalSz = orders.reduce((sum, o) => sum + parseFloat(o.sz), 0);
      console.log(`  $${px.toLocaleString().padStart(12)} │ ${totalSz.toFixed(4).padStart(10)} │ ${orders.length.toString().padStart(2)} orders`);
      // Show first 2 orders at this level
      for (const order of orders.slice(0, 2)) {
        console.log(`               │ └─ ${parseFloat(order.sz).toFixed(4).padStart(10)} (oid: ${order.oid.slice(0, 12)}...)`);
      }
    }

    // Spread
    const spread = this.getSpread();
    console.log(`\n  ${"─".repeat(44)}`);
    console.log(`  SPREAD: $${spread.toLocaleString()}`);
    console.log(`  ${"─".repeat(44)}\n`);

    // Display bids
    console.log(" BIDS:");
    const bidPrices = Array.from(bidByPrice.keys()).sort((a, b) => b - a).slice(0, levels);
    for (const px of bidPrices) {
      const orders = bidByPrice.get(px)!;
      const totalSz = orders.reduce((sum, o) => sum + parseFloat(o.sz), 0);
      console.log(`  $${px.toLocaleString().padStart(12)} │ ${totalSz.toFixed(4).padStart(10)} │ ${orders.length.toString().padStart(2)} orders`);
      for (const order of orders.slice(0, 2)) {
        console.log(`               │ └─ ${parseFloat(order.sz).toFixed(4).padStart(10)} (oid: ${order.oid.slice(0, 12)}...)`);
      }
    }

    // Summary
    console.log("\n SUMMARY:");
    console.log(`  Total Bid Orders: ${String(depth.bidOrders).padStart(6)}`);
    console.log(`  Total Ask Orders: ${String(depth.askOrders).padStart(6)}`);
    console.log(`  Bid Depth (top ${levels}): ${(depth.bidDepth as number).toFixed(4).padStart(10)}`);
    console.log(`  Ask Depth (top ${levels}): ${(depth.askDepth as number).toFixed(4).padStart(10)}`);
  }
}

async function main() {
  console.log("=".repeat(60));
  console.log("L4 ORDER BOOK STREAMING (gRPC)");
  console.log("=".repeat(60));
  console.log(`Endpoint: ${ENDPOINT.slice(0, 50)}...`);
  console.log();
  console.log("L4 book shows individual orders with order IDs.");
  console.log("This is essential for:");
  console.log("  - Market making (queue position)");
  console.log("  - Order flow analysis (large orders)");
  console.log("  - Optimal execution (what you're crossing)");
  console.log();

  // Create book manager
  const book = new L4BookManager("BTC");

  const onL4Update = (data: Record<string, unknown>) => {
    book.processUpdate(data);

    // Display every update for first 5, then every 10th
    if (book.updateCount <= 5 || book.updateCount % 10 === 0) {
      book.display(3);
    }

    if (book.updateCount >= 30) {
      console.log(`\nReceived ${book.updateCount} updates. Stopping...`);
    }
  };

  const onState = (state: GRPCConnectionState) => {
    console.log(`[${timestamp()}] Connection state: ${state}`);
  };

  const onError = (error: unknown) => {
    console.log(`[${timestamp()}] Error: ${error}`);
  };

  const onConnect = () => {
    console.log(`[${timestamp()}] Connected to L4 book stream`);
  };

  // Create gRPC stream
  const stream = new GRPCStream(ENDPOINT, {
    onError,
    onConnect,
    onStateChange: onState,
    reconnect: true,
  });

  // Subscribe to L4 book
  console.log("Subscribing to BTC L4 order book...");
  stream.l4Book("BTC", onL4Update);

  // Handle Ctrl+C
  process.on('SIGINT', () => {
    console.log("\n\nStopping...");
    stream.stop();
    console.log(`\nFinal stats:`);
    console.log(`  Total updates: ${book.updateCount}`);
    console.log(`  Total bid orders: ${book.bids.size}`);
    console.log(`  Total ask orders: ${book.asks.size}`);
    process.exit(0);
  });

  console.log("-".repeat(60));
  console.log("Streaming L4 book... (Ctrl+C to stop)");
  console.log();

  // Start streaming
  await stream.start();

  // Run for 60 seconds or until we have 30 updates
  const start = Date.now();
  while (book.updateCount < 30 && Date.now() - start < 60000) {
    await new Promise(resolve => setTimeout(resolve, 500));
  }

  stream.stop();

  console.log();
  console.log("=".repeat(60));
  console.log("L4 BOOK STREAMING COMPLETE");
  console.log("=".repeat(60));
  console.log(`Total updates received: ${book.updateCount}`);
  console.log(`Final bid orders: ${book.bids.size}`);
  console.log(`Final ask orders: ${book.asks.size}`);
}

main().catch(console.error);
