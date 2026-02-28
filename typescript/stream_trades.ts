#!/usr/bin/env npx ts-node
/**
 * WebSocket Streaming Example — Real-Time HyperCore Data
 *
 * Stream trades, orders, book updates, events, and TWAP via WebSocket.
 * These are the data streams available on QuickNode endpoints.
 *
 * Available QuickNode WebSocket streams:
 * - trades: Executed trades with price, size, direction
 * - orders: Order lifecycle events (open, filled, cancelled)
 * - book_updates: Order book changes (incremental deltas)
 * - events: Balance changes, transfers, deposits, withdrawals
 * - twap: TWAP execution data
 * - writer_actions: HyperCore <-> HyperEVM asset transfers
 *
 * Note: L2/L4 order book snapshots are available via gRPC (see stream_orderbook.ts).
 *       Other streams (allMids, bbo, candle) require the public Hyperliquid API.
 *
 * Setup:
 *     npm install hyperliquid-sdk ws
 *
 * Usage:
 *     export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
 *     npx ts-node stream_trades.ts
 *
 * The SDK handles:
 * - Automatic reconnection with exponential backoff
 * - Ping/pong heartbeats
 * - Connection state management
 * - Subscription resubscription on reconnect
 */

import { Stream, StreamConnectionState } from 'hyperliquid-sdk';

const ENDPOINT = process.env.ENDPOINT;
if (!ENDPOINT) {
  console.log("WebSocket Streaming Example");
  console.log("=".repeat(60));
  console.log();
  console.log("Usage:");
  console.log("  export ENDPOINT='https://YOUR-ENDPOINT.quiknode.pro/TOKEN'");
  console.log("  npx ts-node stream_trades.ts");
  process.exit(1);
}

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
    // QuickNode format: {"type": "data", "stream": "hl.trades", "block": {"events": [...]}}
    // Events are [[user, trade_data], ...]
    const block = (data.block || {}) as Record<string, unknown>;
    for (const event of (block.events || []) as unknown[]) {
      if (Array.isArray(event) && event.length >= 2) {
        const t = event[1] as Record<string, unknown>;
        tradeCount++;
        const coin = t.coin || "?";
        const px = parseFloat(String(t.px || 0));
        const sz = t.sz || "?";
        const side = t.side === "B" ? "BUY " : "SELL";
        console.log(`[${timestamp()}] ${side} ${sz} ${coin} @ $${px.toLocaleString()}`);

        if (tradeCount >= 5) {
          console.log(`\nReceived ${tradeCount} trades. Moving to next example...`);
          return;
        }
      }
    }
  };

  const stream = new Stream(ENDPOINT, { reconnect: false });
  stream.trades(["BTC", "ETH"], onTrade);

  console.log("Subscribing to BTC and ETH trades...");
  console.log("-".repeat(60));

  await stream.start();

  const start = Date.now();
  while (tradeCount < 5 && Date.now() - start < 20000) {
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  stream.stop();
  console.log(`Total trades received: ${tradeCount}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXAMPLE 2: Stream Orders
// ═══════════════════════════════════════════════════════════════════════════════

async function streamOrdersExample(): Promise<void> {
  console.log("\n" + "=".repeat(60));
  console.log("EXAMPLE 2: Streaming Orders");
  console.log("=".repeat(60));
  console.log();
  console.log("Order events: open, filled, triggered, canceled, etc.");
  console.log();

  let orderCount = 0;

  const onOrder = (data: Record<string, unknown>) => {
    const block = (data.block || {}) as Record<string, unknown>;
    for (const event of (block.events || []) as unknown[]) {
      if (Array.isArray(event) && event.length >= 2) {
        const o = event[1] as Record<string, unknown>;
        orderCount++;
        const coin = o.coin || "?";
        const status = o.status || "?";
        const side = o.side === "B" ? "BUY" : "SELL";
        const px = o.px || "?";
        const sz = o.sz || "?";
        console.log(`[${timestamp()}] ${status}: ${side} ${sz} ${coin} @ $${px}`);

        if (orderCount >= 10) {
          console.log(`\nReceived ${orderCount} orders. Moving to next example...`);
          return;
        }
      }
    }
  };

  const stream = new Stream(ENDPOINT, { reconnect: false });
  stream.orders(["BTC", "ETH"], onOrder);

  console.log("Subscribing to BTC and ETH orders...");
  console.log("-".repeat(60));

  await stream.start();

  const start = Date.now();
  while (orderCount < 10 && Date.now() - start < 20000) {
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  stream.stop();
  console.log(`Total orders received: ${orderCount}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXAMPLE 3: Stream Book Updates (Incremental)
// ═══════════════════════════════════════════════════════════════════════════════

async function streamBookUpdatesExample(): Promise<void> {
  console.log("\n" + "=".repeat(60));
  console.log("EXAMPLE 3: Streaming Book Updates (Incremental)");
  console.log("=".repeat(60));
  console.log();
  console.log("Book updates show individual order changes to the order book.");
  console.log("Each event contains: user, oid, coin, side, px, raw_book_diff");
  console.log();

  let updateCount = 0;

  const onBookUpdate = (data: Record<string, unknown>) => {
    const block = (data.block || {}) as Record<string, unknown>;
    const events = (block.events || []) as Record<string, unknown>[];

    if (events.length) {
      updateCount++;
      // Show first event from this block
      const event = events[0];
      const coin = event.coin || "?";
      const side = event.side === "B" ? "BID" : "ASK";
      const px = event.px || "?";
      const diff = event.raw_book_diff;

      let action: string;
      let sz: string;
      if (diff === "remove") {
        action = "REMOVE";
        sz = "-";
      } else {
        action = "ADD/UPDATE";
        const diffObj = diff as Record<string, unknown> | undefined;
        const newObj = (diffObj?.new || {}) as Record<string, unknown>;
        sz = String(newObj.sz || "?");
      }

      console.log(`[${timestamp()}] ${coin} ${side} @ $${px}: ${action} size=${sz} (+${events.length - 1} more)`);

      if (updateCount >= 10) {
        console.log(`\nReceived ${updateCount} blocks. Moving to next example...`);
      }
    }
  };

  const stream = new Stream(ENDPOINT, { reconnect: false });
  stream.bookUpdates(["BTC"], onBookUpdate);

  console.log("Subscribing to BTC book updates...");
  console.log("-".repeat(60));

  await stream.start();

  const start = Date.now();
  while (updateCount < 10 && Date.now() - start < 20000) {
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  stream.stop();
  console.log(`Total book update blocks received: ${updateCount}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXAMPLE 4: Stream Events
// ═══════════════════════════════════════════════════════════════════════════════

async function streamEventsExample(): Promise<void> {
  console.log("\n" + "=".repeat(60));
  console.log("EXAMPLE 4: Streaming Events");
  console.log("=".repeat(60));
  console.log();
  console.log("Events: balance changes, transfers, deposits, withdrawals, vault ops");
  console.log();

  let eventCount = 0;

  const onEvent = (data: Record<string, unknown>) => {
    const block = (data.block || {}) as Record<string, unknown>;
    const events = (block.events || []) as unknown[];

    for (const event of events) {
      eventCount++;
      // Event structure varies by type
      let eventType = "unknown";
      if (typeof event === 'object' && event !== null) {
        const e = event as Record<string, unknown>;
        if ("deposit" in e) {
          eventType = "deposit";
        } else if ("withdraw" in e) {
          eventType = "withdraw";
        } else if ("transfer" in e) {
          eventType = "transfer";
        } else if ("funding" in e) {
          eventType = "funding";
        } else if ("liquidation" in e) {
          eventType = "liquidation";
        } else {
          const keys = Object.keys(e);
          eventType = keys.length > 0 ? keys[0] : "unknown";
        }
      }

      console.log(`[${timestamp()}] Event #${eventCount}: ${eventType}`);

      if (eventCount >= 5) {
        console.log(`\nReceived ${eventCount} events. Moving to next example...`);
        return;
      }
    }
  };

  const stream = new Stream(ENDPOINT, { reconnect: false });
  stream.events(onEvent);

  console.log("Subscribing to all events...");
  console.log("-".repeat(60));

  await stream.start();

  const start = Date.now();
  while (eventCount < 5 && Date.now() - start < 30000) {
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  stream.stop();
  console.log(`Total events received: ${eventCount}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXAMPLE 5: Multiple Subscriptions with Connection Management
// ═══════════════════════════════════════════════════════════════════════════════

async function multiStreamExample(): Promise<void> {
  console.log("\n" + "=".repeat(60));
  console.log("EXAMPLE 5: Multiple Subscriptions + Connection Management");
  console.log("=".repeat(60));

  const counts = { trades: 0, orders: 0, book: 0 };

  const onTrade = (data: Record<string, unknown>) => {
    counts.trades++;
    const block = (data.block || {}) as Record<string, unknown>;
    const events = (block.events || []) as unknown[];
    if (events.length && Array.isArray(events[0]) && events[0].length >= 2) {
      const t = events[0][1] as Record<string, unknown>;
      const coin = t.coin || "?";
      console.log(`[TRADE] ${coin} - Total: ${counts.trades}`);
    }
  };

  const onOrder = (data: Record<string, unknown>) => {
    counts.orders++;
    const block = (data.block || {}) as Record<string, unknown>;
    const events = (block.events || []) as unknown[];
    if (events.length && Array.isArray(events[0]) && events[0].length >= 2) {
      const o = events[0][1] as Record<string, unknown>;
      const coin = o.coin || "?";
      const status = o.status || "?";
      console.log(`[ORDER] ${coin} ${status} - Total: ${counts.orders}`);
    }
  };

  const onBook = (data: Record<string, unknown>) => {
    counts.book++;
    const block = (data.block || {}) as Record<string, unknown>;
    const events = (block.events || []) as Record<string, unknown>[];
    if (events.length) {
      const coin = events[0].coin || "?";
      console.log(`[BOOK]  ${coin} changes: ${events.length} - Total blocks: ${counts.book}`);
    }
  };

  const onState = (state: StreamConnectionState) => {
    console.log(`[STATE] ${state}`);
  };

  const onOpen = () => {
    console.log("[CONNECTED] WebSocket ready");
  };

  const onError = (error: unknown) => {
    console.log(`[ERROR] ${error}`);
  };

  const stream = new Stream(ENDPOINT, {
    onError,
    onOpen,
    onStateChange: onState,
    reconnect: true,
    maxReconnectAttempts: 3,
  });

  // Multiple subscriptions (all QuickNode-supported)
  stream.trades(["BTC", "ETH"], onTrade);
  stream.orders(["BTC"], onOrder);
  stream.bookUpdates(["BTC"], onBook);

  console.log("Subscribing to trades, orders, and book updates...");
  console.log("-".repeat(60));

  process.on('SIGINT', () => {
    console.log("\nStopping...");
    stream.stop();
    process.exit(0);
  });

  await stream.start();

  // Run for 15 seconds
  await new Promise(resolve => setTimeout(resolve, 15000));

  stream.stop();

  console.log();
  console.log("=".repeat(60));
  console.log("SUMMARY");
  console.log("=".repeat(60));
  console.log(`  Trades received:     ${counts.trades}`);
  console.log(`  Orders received:     ${counts.orders}`);
  console.log(`  Book update blocks:  ${counts.book}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// AVAILABLE STREAMS INFO
// ═══════════════════════════════════════════════════════════════════════════════

function streamsInfo(): void {
  console.log("\n" + "=".repeat(60));
  console.log("AVAILABLE QUICKNODE WEBSOCKET STREAMS");
  console.log("=".repeat(60));
  console.log();
  console.log("HyperCore Data Streams:");
  console.log();
  console.log("  stream.trades(coins, callback)");
  console.log("    - Executed trades with price, size, direction");
  console.log();
  console.log("  stream.orders(coins, callback)");
  console.log("    - Order lifecycle: open, filled, triggered, canceled");
  console.log();
  console.log("  stream.bookUpdates(coins, callback)");
  console.log("    - Incremental order book changes (deltas)");
  console.log();
  console.log("  stream.events(callback)");
  console.log("    - Balance changes, transfers, deposits, withdrawals");
  console.log();
  console.log("  stream.twap(coins, callback)");
  console.log("    - TWAP execution data and progress");
  console.log();
  console.log("  stream.writerActions(callback)");
  console.log("    - HyperCore <-> HyperEVM asset transfers");
  console.log();
  console.log("For L2/L4 Order Books:");
  console.log("  Use gRPC streaming (see stream_orderbook.ts)");
  console.log("  - StreamL2Book: Aggregated price levels");
  console.log("  - StreamL4Book: Individual orders with order IDs");
  console.log();
  console.log("Example with filtering:");
  console.log("  stream.trades(['BTC', 'ETH'], (t) => console.log(t))");
  console.log();
}

// ═══════════════════════════════════════════════════════════════════════════════
// MAIN
// ═══════════════════════════════════════════════════════════════════════════════

async function main() {
  console.log("=".repeat(60));
  console.log("WebSocket Streaming Examples (QuickNode)");
  console.log("=".repeat(60));
  console.log(`Endpoint: ${ENDPOINT.slice(0, 50)}...`);
  console.log();
  console.log("This demo shows QuickNode WebSocket streaming capabilities:");
  console.log("  1. Trades - Real-time executed trades");
  console.log("  2. Orders - Order lifecycle events");
  console.log("  3. Book Updates - Incremental order book changes");
  console.log("  4. Events - Balance changes, transfers, etc.");
  console.log("  5. Multi-stream - Multiple subscriptions");
  console.log();

  try {
    await streamTradesExample();
    await streamOrdersExample();
    await streamBookUpdatesExample();
    await streamEventsExample();
    // await multiStreamExample();  // Uncomment for full demo

    // Show available streams info
    streamsInfo();

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
