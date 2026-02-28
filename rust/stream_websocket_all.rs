//! WebSocket Streaming — Complete Reference
//!
//! This example demonstrates ALL WebSocket subscription types:
//! - Market Data: trades, l2_book, book_updates, all_mids, candle, bbo
//! - User Data: open_orders, user_fills, user_fundings, clearinghouse_state
//! - TWAP: twap, twap_states, user_twap_slice_fills
//! - System: events, notification
//!
//! # Usage
//! ```bash
//! export ENDPOINT=https://your-endpoint.hype-mainnet.quiknode.pro/TOKEN
//! export USER_ADDRESS=0x...  # Optional, for user data streams
//! cargo run --example stream_websocket_all
//! ```

use hyperliquid_sdk::Stream;
use std::collections::HashMap;
use std::sync::{Arc, RwLock};
use std::sync::atomic::{AtomicUsize, Ordering};
use std::time::Duration;
use tokio::time::sleep;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();

    let endpoint = std::env::var("ENDPOINT").expect("Set ENDPOINT environment variable");
    let user = std::env::var("USER_ADDRESS")
        .unwrap_or_else(|_| "0x0000000000000000000000000000000000000000".to_string());

    println!("==================================================");
    println!("WebSocket Streaming — Complete Reference");
    println!("==================================================");
    println!("Endpoint: {}...", &endpoint[..50.min(endpoint.len())]);
    println!();

    // Print reference table
    print_reference();

    // Run demos
    demo_market_data(&endpoint).await?;
    demo_user_data(&endpoint, &user).await?;
    demo_twap(&endpoint).await?;
    demo_system(&endpoint).await?;
    demo_connection_management(&endpoint).await?;

    println!();
    println!("==================================================");
    println!("All WebSocket examples completed!");
    println!("==================================================");

    Ok(())
}

fn print_reference() {
    println!("\n==================================================");
    println!("WEBSOCKET SUBSCRIPTION REFERENCE");
    println!("==================================================");
    println!();
    println!("┌────────────────────────┬────────────────────────────────────────┐");
    println!("│ Method                 │ Description                            │");
    println!("├────────────────────────┼────────────────────────────────────────┤");
    println!("│ MARKET DATA            │                                        │");
    println!("│ trades(coins, cb)      │ Executed trades                        │");
    println!("│ book_updates(coins,cb) │ Order book deltas                      │");
    println!("│ l2_book(coin, cb)      │ Full L2 order book                     │");
    println!("│ all_mids(cb)           │ All asset mid prices                   │");
    println!("│ candle(coin,int,cb)    │ OHLCV candles (1m,5m,15m,1h,4h,1d)     │");
    println!("│ bbo(coin, cb)          │ Best bid/offer                         │");
    println!("│ active_asset_ctx(c,cb) │ Asset context (funding, OI)            │");
    println!("├────────────────────────┼────────────────────────────────────────┤");
    println!("│ USER DATA              │                                        │");
    println!("│ orders(coins,cb,users) │ Order lifecycle (filtered)             │");
    println!("│ open_orders(user, cb)  │ User's open orders                     │");
    println!("│ order_updates(user,cb) │ Order status changes                   │");
    println!("│ user_events(user, cb)  │ All user events                        │");
    println!("│ user_fills(user, cb)   │ Trade fills                            │");
    println!("│ user_fundings(user,cb) │ Funding payments                       │");
    println!("│ clearinghouse..(u,cb)  │ Positions/margin                       │");
    println!("├────────────────────────┼────────────────────────────────────────┤");
    println!("│ TWAP                   │                                        │");
    println!("│ twap(coins, cb)        │ TWAP execution                         │");
    println!("│ twap_states(user, cb)  │ TWAP algorithm states                  │");
    println!("├────────────────────────┼────────────────────────────────────────┤");
    println!("│ SYSTEM                 │                                        │");
    println!("│ events(cb)             │ Funding, liquidations                  │");
    println!("│ writer_actions(cb)     │ Spot token transfers                   │");
    println!("│ notification(user,cb)  │ User notifications                     │");
    println!("└────────────────────────┴────────────────────────────────────────┘");
    println!();
}

async fn demo_market_data(endpoint: &str) -> Result<(), Box<dyn std::error::Error>> {
    println!("\n==================================================");
    println!("MARKET DATA STREAMS");
    println!("==================================================");
    println!();
    println!("Available streams:");
    println!("  - trades(coins, callback)");
    println!("  - book_updates(coins, callback)");
    println!("  - l2_book(coin, callback)");
    println!("  - all_mids(callback)");
    println!("  - bbo(coin, callback)");
    println!();

    let counts: Arc<RwLock<HashMap<String, usize>>> = Arc::new(RwLock::new(HashMap::new()));

    let mut stream = Stream::new(endpoint)?;

    // trades
    let c = counts.clone();
    stream.on_trade(move |_data| {
        if let Ok(mut m) = c.write() {
            *m.entry("trades".to_string()).or_insert(0) += 1;
            let count = m["trades"];
            if count <= 3 {
                println!("[TRADES] Message #{}", count);
            }
        }
    });

    // book_updates
    let c = counts.clone();
    stream.on_book_update(move |_data| {
        if let Ok(mut m) = c.write() {
            *m.entry("book_updates".to_string()).or_insert(0) += 1;
            let count = m["book_updates"];
            if count <= 3 {
                println!("[BOOK_UPDATES] Message #{}", count);
            }
        }
    });

    // l2_book
    let c = counts.clone();
    stream.on_l2_book(move |_data| {
        if let Ok(mut m) = c.write() {
            *m.entry("l2_book".to_string()).or_insert(0) += 1;
            let count = m["l2_book"];
            if count <= 3 {
                println!("[L2_BOOK] Message #{}", count);
            }
        }
    });

    // all_mids
    let c = counts.clone();
    stream.on_all_mids(move |_data| {
        if let Ok(mut m) = c.write() {
            *m.entry("all_mids".to_string()).or_insert(0) += 1;
            let count = m["all_mids"];
            if count <= 3 {
                println!("[ALL_MIDS] Message #{}", count);
            }
        }
    });

    // bbo
    let c = counts.clone();
    stream.on_bbo(move |_data| {
        if let Ok(mut m) = c.write() {
            *m.entry("bbo".to_string()).or_insert(0) += 1;
            let count = m["bbo"];
            if count <= 3 {
                println!("[BBO] Message #{}", count);
            }
        }
    });

    stream.subscribe_trades(&["BTC", "ETH"]).await?;
    stream.subscribe_book_updates(&["BTC"]).await?;
    stream.subscribe_l2_book("BTC").await?;
    stream.subscribe_all_mids().await?;
    stream.subscribe_bbo("ETH").await?;

    println!("Subscribing to market data streams...");
    println!("------------------------------------------------------------");

    sleep(Duration::from_secs(10)).await;

    stream.stop().await?;

    println!();
    println!("Market data summary:");
    if let Ok(m) = counts.read() {
        for name in &["trades", "book_updates", "l2_book", "all_mids", "bbo"] {
            println!("  {}: {} messages", name, m.get(*name).unwrap_or(&0));
        }
    }

    Ok(())
}

async fn demo_user_data(endpoint: &str, user: &str) -> Result<(), Box<dyn std::error::Error>> {
    println!("\n==================================================");
    println!("USER DATA STREAMS");
    println!("==================================================");
    println!();
    println!("User address: {}", user);
    println!();
    println!("Available streams:");
    println!("  - orders(coins, callback, users)");
    println!("  - open_orders(user, callback)");
    println!("  - user_fills(user, callback)");
    println!("  - user_fundings(user, callback)");
    println!("  - clearinghouse_state(user, callback)");
    println!();

    if user == "0x0000000000000000000000000000000000000000" {
        println!("NOTE: Set USER_ADDRESS env var for real user data.");
        println!("      Skipping user data demo.");
        return Ok(());
    }

    let counts: Arc<RwLock<HashMap<String, usize>>> = Arc::new(RwLock::new(HashMap::new()));

    let mut stream = Stream::new(endpoint)?;

    let c = counts.clone();
    stream.on_order(move |_data| {
        if let Ok(mut m) = c.write() {
            *m.entry("orders".to_string()).or_insert(0) += 1;
        }
    });

    stream.subscribe_orders(&["BTC", "ETH"], Some(vec![user.to_string()])).await?;

    println!("Subscribing to user data streams...");
    println!("------------------------------------------------------------");

    sleep(Duration::from_secs(10)).await;

    stream.stop().await?;

    println!();
    println!("User data summary:");
    if let Ok(m) = counts.read() {
        for name in &["orders", "open_orders", "user_fills", "user_fundings", "clearinghouse"] {
            println!("  {}: {} messages", name, m.get(*name).unwrap_or(&0));
        }
    }

    Ok(())
}

async fn demo_twap(endpoint: &str) -> Result<(), Box<dyn std::error::Error>> {
    println!("\n==================================================");
    println!("TWAP STREAMS");
    println!("==================================================");
    println!();
    println!("Available streams:");
    println!("  - twap(coins, callback)");
    println!("  - twap_states(user, callback)");
    println!();

    let twap_count = Arc::new(AtomicUsize::new(0));
    let twap_count_clone = twap_count.clone();

    let mut stream = Stream::new(endpoint)?;

    stream.on_twap(move |_data| {
        twap_count_clone.fetch_add(1, Ordering::SeqCst);
    });

    stream.subscribe_twap(&["BTC", "ETH"]).await?;

    println!("Subscribing to TWAP streams...");
    println!("------------------------------------------------------------");

    sleep(Duration::from_secs(5)).await;

    stream.stop().await?;

    println!();
    println!("TWAP summary:");
    println!("  twap: {} messages", twap_count.load(Ordering::SeqCst));

    Ok(())
}

async fn demo_system(endpoint: &str) -> Result<(), Box<dyn std::error::Error>> {
    println!("\n==================================================");
    println!("SYSTEM STREAMS");
    println!("==================================================");
    println!();
    println!("Available streams:");
    println!("  - events(callback)");
    println!("  - writer_actions(callback)");
    println!();

    let events_count = Arc::new(AtomicUsize::new(0));
    let events_count_clone = events_count.clone();

    let mut stream = Stream::new(endpoint)?;

    stream.on_event(move |_data| {
        events_count_clone.fetch_add(1, Ordering::SeqCst);
    });

    stream.subscribe_events().await?;

    println!("Subscribing to system streams...");
    println!("------------------------------------------------------------");

    sleep(Duration::from_secs(5)).await;

    stream.stop().await?;

    println!();
    println!("System summary:");
    println!("  events: {} messages", events_count.load(Ordering::SeqCst));

    Ok(())
}

async fn demo_connection_management(endpoint: &str) -> Result<(), Box<dyn std::error::Error>> {
    println!("\n==================================================");
    println!("CONNECTION MANAGEMENT");
    println!("==================================================");
    println!();
    println!("Available callbacks:");
    println!("  - on_open: Called when connected");
    println!("  - on_close: Called when disconnected");
    println!("  - on_error: Called on errors");
    println!("  - on_reconnect: Called on reconnection");
    println!("  - on_state_change: Called on state changes");
    println!();
    println!("Properties:");
    println!("  - stream.connected(): bool");
    println!("  - stream.state(): ConnectionState");
    println!();

    let mut stream = Stream::new(endpoint)?;

    stream.on_open(|| {
        println!("[CONNECTED]");
    });

    stream.on_close(|| {
        println!("[CLOSED]");
    });

    stream.on_error(|error| {
        println!("[ERROR] {}", error);
    });

    stream.on_trade(|_data| {
        // Just for testing
    });

    stream.subscribe_trades(&["BTC"]).await?;

    println!("Testing connection management...");
    println!("------------------------------------------------------------");

    println!("  Connected: {}", stream.connected());

    sleep(Duration::from_secs(5)).await;

    stream.stop().await?;

    println!("\n  Final state: disconnected");

    Ok(())
}
