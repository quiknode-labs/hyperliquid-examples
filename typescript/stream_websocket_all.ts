#!/usr/bin/env npx ts-node
/**
 * WebSocket Streaming — Complete Reference
 *
 * This example demonstrates ALL WebSocket subscription types:
 * - Market Data: trades, l2_book, book_updates, all_mids, candle, bbo
 * - User Data: open_orders, user_fills, user_fundings, clearinghouse_state
 * - TWAP: twap, twap_states, user_twap_slice_fills
 * - System: events, notification
 *
 * Setup:
 *     npm install hyperliquid-sdk ws
 *
 * Usage:
 *     export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
 *     npx ts-node stream_websocket_all.ts
 */

import { Stream, StreamConnectionState } from 'hyperliquid-sdk';

const ENDPOINT = process.env.ENDPOINT;
const USER = process.env.USER_ADDRESS || "0x0000000000000000000000000000000000000000";

if (!ENDPOINT) {
  console.log("WebSocket Complete Reference");
  console.log("=".repeat(60));
  console.log();
  console.log("Usage:");
  console.log("  export ENDPOINT='https://YOUR-ENDPOINT.quiknode.pro/TOKEN'");
  console.log("  export USER_ADDRESS='0x...'  # Optional, for user data streams");
  console.log("  npx ts-node stream_websocket_all.ts");
  process.exit(1);
}

function timestamp(): string {
  const now = new Date();
  return now.toTimeString().split(' ')[0] + '.' + String(now.getMilliseconds()).padStart(3, '0');
}

// Global counters
const counts: Record<string, number> = {};

function makeCallback(name: string, maxPrints: number = 3): (data: Record<string, unknown>) => void {
  counts[name] = 0;

  return (data: Record<string, unknown>) => {
    counts[name]++;
    if (counts[name] <= maxPrints) {
      const channel = data.channel || "unknown";
      console.log(`[${timestamp()}] ${name.toUpperCase()}: ${channel} (#${counts[name]})`);
      // Print first few fields of data
      const innerData = data.data || data;
      if (typeof innerData === 'object' && innerData !== null && !Array.isArray(innerData)) {
        const keys = Object.keys(innerData as Record<string, unknown>).slice(0, 3);
        console.log(`             Fields: ${JSON.stringify(keys)}`);
      } else if (Array.isArray(innerData) && innerData.length) {
        console.log(`             Items: ${innerData.length}`);
      }
    }
  };
}

// ═══════════════════════════════════════════════════════════════════════════════
// MARKET DATA STREAMS
// ═══════════════════════════════════════════════════════════════════════════════

async function demoMarketData(): Promise<void> {
  console.log("\n" + "=".repeat(60));
  console.log("MARKET DATA STREAMS");
  console.log("=".repeat(60));
  console.log();
  console.log("Available streams:");
  console.log("  - trades(coins, callback)");
  console.log("  - bookUpdates(coins, callback)");
  console.log("  - l2Book(coin, callback)");
  console.log("  - allMids(callback)");
  console.log("  - candle(coin, interval, callback)");
  console.log("  - bbo(coin, callback)");
  console.log("  - activeAssetCtx(coin, callback)");
  console.log();

  const stream = new Stream(ENDPOINT, { reconnect: false });

  // trades: Real-time executed trades
  stream.trades(["BTC", "ETH"], makeCallback("trades"));

  // bookUpdates: Incremental order book changes
  stream.bookUpdates(["BTC"], makeCallback("book_updates"));

  // l2Book: Full L2 order book snapshots
  stream.l2Book("BTC", makeCallback("l2_book"));

  // allMids: All asset mid prices
  stream.allMids(makeCallback("all_mids"));

  // bbo: Best bid/offer updates
  stream.bbo("ETH", makeCallback("bbo"));

  // activeAssetCtx: Asset context (funding, OI, volume)
  stream.activeAssetCtx("BTC", makeCallback("asset_ctx"));

  console.log("Subscribing to market data streams...");
  console.log("-".repeat(60));

  await stream.start();

  // Wait for messages
  await new Promise(resolve => setTimeout(resolve, 10000));

  stream.stop();

  console.log();
  console.log("Market data summary:");
  for (const name of ["trades", "book_updates", "l2_book", "all_mids", "bbo", "asset_ctx"]) {
    console.log(`  ${name}: ${counts[name] || 0} messages`);
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// USER DATA STREAMS (requires user address)
// ═══════════════════════════════════════════════════════════════════════════════

async function demoUserData(): Promise<void> {
  console.log("\n" + "=".repeat(60));
  console.log("USER DATA STREAMS");
  console.log("=".repeat(60));
  console.log();
  console.log(`User address: ${USER}`);
  console.log();
  console.log("Available streams:");
  console.log("  - orders(coins, callback, { users: [...] })");
  console.log("  - openOrders(user, callback)");
  console.log("  - orderUpdates(user, callback)");
  console.log("  - userEvents(user, callback)");
  console.log("  - userFills(user, callback)");
  console.log("  - userFundings(user, callback)");
  console.log("  - userNonFundingLedger(user, callback)");
  console.log("  - clearinghouseState(user, callback)");
  console.log("  - activeAssetData(user, coin, callback)");
  console.log();

  if (USER === "0x0000000000000000000000000000000000000000") {
    console.log("NOTE: Set USER_ADDRESS env var for real user data.");
    console.log("      Skipping user data demo.");
    return;
  }

  const stream = new Stream(ENDPOINT, { reconnect: false });

  // orders: Order lifecycle for specific user
  stream.orders(["BTC", "ETH"], makeCallback("orders"), { users: [USER] });

  // openOrders: User's open orders
  stream.openOrders(USER, makeCallback("open_orders"));

  // userFills: Trade fills
  stream.userFills(USER, makeCallback("user_fills"));

  // userFundings: Funding payments
  stream.userFundings(USER, makeCallback("user_fundings"));

  // clearinghouseState: Positions and margin
  stream.clearinghouseState(USER, makeCallback("clearinghouse"));

  console.log("Subscribing to user data streams...");
  console.log("-".repeat(60));

  await stream.start();

  await new Promise(resolve => setTimeout(resolve, 10000));

  stream.stop();

  console.log();
  console.log("User data summary:");
  for (const name of ["orders", "open_orders", "user_fills", "user_fundings", "clearinghouse"]) {
    console.log(`  ${name}: ${counts[name] || 0} messages`);
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// TWAP STREAMS
// ═══════════════════════════════════════════════════════════════════════════════

async function demoTwap(): Promise<void> {
  console.log("\n" + "=".repeat(60));
  console.log("TWAP STREAMS");
  console.log("=".repeat(60));
  console.log();
  console.log("Available streams:");
  console.log("  - twap(coins, callback)");
  console.log("  - twapStates(user, callback)");
  console.log("  - userTwapSliceFills(user, callback)");
  console.log("  - userTwapHistory(user, callback)");
  console.log();

  const stream = new Stream(ENDPOINT, { reconnect: false });

  // twap: TWAP execution updates
  stream.twap(["BTC", "ETH"], makeCallback("twap"));

  console.log("Subscribing to TWAP streams...");
  console.log("-".repeat(60));

  await stream.start();

  await new Promise(resolve => setTimeout(resolve, 5000));

  stream.stop();

  console.log();
  console.log("TWAP summary:");
  console.log(`  twap: ${counts.twap || 0} messages`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// SYSTEM STREAMS
// ═══════════════════════════════════════════════════════════════════════════════

async function demoSystem(): Promise<void> {
  console.log("\n" + "=".repeat(60));
  console.log("SYSTEM STREAMS");
  console.log("=".repeat(60));
  console.log();
  console.log("Available streams:");
  console.log("  - events(callback)");
  console.log("  - writerActions(callback)");
  console.log("  - notification(user, callback)");
  console.log("  - webData3(user, callback)");
  console.log();

  const stream = new Stream(ENDPOINT, { reconnect: false });

  // events: System events (funding, liquidations)
  stream.events(makeCallback("events"));

  // writerActions: Spot token transfers
  stream.writerActions(makeCallback("writer_actions"));

  console.log("Subscribing to system streams...");
  console.log("-".repeat(60));

  await stream.start();

  await new Promise(resolve => setTimeout(resolve, 5000));

  stream.stop();

  console.log();
  console.log("System summary:");
  for (const name of ["events", "writer_actions"]) {
    console.log(`  ${name}: ${counts[name] || 0} messages`);
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// CONNECTION MANAGEMENT
// ═══════════════════════════════════════════════════════════════════════════════

async function demoConnectionManagement(): Promise<void> {
  console.log("\n" + "=".repeat(60));
  console.log("CONNECTION MANAGEMENT");
  console.log("=".repeat(60));
  console.log();
  console.log("Available callbacks:");
  console.log("  - onOpen: Called when connected");
  console.log("  - onClose: Called when disconnected");
  console.log("  - onError: Called on errors");
  console.log("  - onReconnect: Called on reconnection");
  console.log("  - onStateChange: Called on state changes");
  console.log();
  console.log("Properties:");
  console.log("  - stream.connected: boolean");
  console.log("  - stream.state: ConnectionState");
  console.log("  - stream.reconnectAttempts: number");
  console.log();

  const onOpen = () => {
    console.log(`[${timestamp()}] CONNECTED`);
  };

  const onClose = () => {
    console.log(`[${timestamp()}] CLOSED`);
  };

  const onError = (error: unknown) => {
    console.log(`[${timestamp()}] ERROR: ${error}`);
  };

  const onStateChange = (state: StreamConnectionState) => {
    console.log(`[${timestamp()}] STATE: ${state}`);
  };

  const stream = new Stream(ENDPOINT, {
    onOpen,
    onClose,
    onError,
    onStateChange,
    reconnect: true,
    maxReconnectAttempts: 3,
  });

  stream.trades(["BTC"], makeCallback("conn_test"));

  console.log("Testing connection management...");
  console.log("-".repeat(60));

  await stream.start();

  console.log(`  Connected: ${stream.connected}`);
  console.log(`  State: ${stream.state}`);

  await new Promise(resolve => setTimeout(resolve, 5000));

  stream.stop();

  console.log(`\n  Final state: ${stream.state}`);
}

// ═══════════════════════════════════════════════════════════════════════════════
// REFERENCE TABLE
// ═══════════════════════════════════════════════════════════════════════════════

function printReference(): void {
  console.log("\n" + "=".repeat(60));
  console.log("WEBSOCKET SUBSCRIPTION REFERENCE");
  console.log("=".repeat(60));
  console.log();
  console.log("┌────────────────────────┬────────────────────────────────────────┐");
  console.log("│ Method                 │ Description                            │");
  console.log("├────────────────────────┼────────────────────────────────────────┤");
  console.log("│ MARKET DATA            │                                        │");
  console.log("│ trades(coins, cb)      │ Executed trades                        │");
  console.log("│ bookUpdates(coins,cb)  │ Order book deltas                      │");
  console.log("│ l2Book(coin, cb)       │ Full L2 order book                     │");
  console.log("│ allMids(cb)            │ All asset mid prices                   │");
  console.log("│ candle(coin,int,cb)    │ OHLCV candles (1m,5m,15m,1h,4h,1d)     │");
  console.log("│ bbo(coin, cb)          │ Best bid/offer                         │");
  console.log("│ activeAssetCtx(c,cb)   │ Asset context (funding, OI)            │");
  console.log("├────────────────────────┼────────────────────────────────────────┤");
  console.log("│ USER DATA              │                                        │");
  console.log("│ orders(coins,cb,users) │ Order lifecycle (filtered)             │");
  console.log("│ openOrders(user, cb)   │ User's open orders                     │");
  console.log("│ orderUpdates(user,cb)  │ Order status changes                   │");
  console.log("│ userEvents(user, cb)   │ All user events                        │");
  console.log("│ userFills(user, cb)    │ Trade fills                            │");
  console.log("│ userFundings(user,cb)  │ Funding payments                       │");
  console.log("│ userNonFund..(u,cb)    │ Ledger updates                         │");
  console.log("│ clearinghouse..(u,cb)  │ Positions/margin                       │");
  console.log("│ activeAsset..(u,c,cb)  │ User trading params                    │");
  console.log("├────────────────────────┼────────────────────────────────────────┤");
  console.log("│ TWAP                   │                                        │");
  console.log("│ twap(coins, cb)        │ TWAP execution                         │");
  console.log("│ twapStates(user, cb)   │ TWAP algorithm states                  │");
  console.log("│ userTwapSlice..(u,c)   │ TWAP slice fills                       │");
  console.log("│ userTwapHist..(u,cb)   │ TWAP history                           │");
  console.log("├────────────────────────┼────────────────────────────────────────┤");
  console.log("│ SYSTEM                 │                                        │");
  console.log("│ events(cb)             │ Funding, liquidations                  │");
  console.log("│ writerActions(cb)      │ Spot token transfers                   │");
  console.log("│ notification(user,cb)  │ User notifications                     │");
  console.log("│ webData3(user, cb)     │ Aggregate user info                    │");
  console.log("└────────────────────────┴────────────────────────────────────────┘");
  console.log();
}

// ═══════════════════════════════════════════════════════════════════════════════
// MAIN
// ═══════════════════════════════════════════════════════════════════════════════

async function main() {
  console.log("=".repeat(60));
  console.log("WebSocket Streaming — Complete Reference");
  console.log("=".repeat(60));
  console.log(`Endpoint: ${ENDPOINT.slice(0, 50)}...`);
  console.log();

  // Handle Ctrl+C
  process.on('SIGINT', () => {
    console.log("\nDemo interrupted.");
    process.exit(0);
  });

  try {
    // Print reference table
    printReference();

    // Run demos
    await demoMarketData();
    await demoUserData();
    await demoTwap();
    await demoSystem();
    await demoConnectionManagement();

    console.log();
    console.log("=".repeat(60));
    console.log("All WebSocket examples completed!");
    console.log("=".repeat(60));
    console.log();
    console.log("Total messages received:");
    for (const [name, count] of Object.entries(counts).sort()) {
      console.log(`  ${name}: ${count}`);
    }

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
