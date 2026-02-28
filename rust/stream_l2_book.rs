//! L2 Order Book Streaming — Aggregated Price Levels
//!
//! L2 order book shows total size at each price level (aggregated).
//! Available via both WebSocket and gRPC.
//!
//! Use L2 for:
//! - Price monitoring
//! - Basic trading strategies
//! - Lower bandwidth requirements
//!
//! Use L4 (gRPC only) when you need:
//! - Individual order IDs
//! - Queue position tracking
//! - Order flow analysis
//!
//! # Usage
//! ```bash
//! export ENDPOINT=https://your-endpoint.hype-mainnet.quiknode.pro/TOKEN
//! cargo run --example stream_l2_book
//! ```

use hyperliquid_sdk::{GRPCStream, Stream};
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;
use std::time::Duration;
use tokio::time::sleep;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();

    let endpoint = std::env::var("ENDPOINT").expect("Set ENDPOINT environment variable");

    println!("==================================================");
    println!("L2 ORDER BOOK STREAMING");
    println!("==================================================");
    println!("Endpoint: {}...", &endpoint[..50.min(endpoint.len())]);

    // Show comparison
    compare_sources();

    // Stream via gRPC
    stream_l2_grpc(&endpoint).await?;

    // Stream via WebSocket
    stream_l2_websocket(&endpoint).await?;

    println!();
    println!("==================================================");
    println!("All L2 examples completed!");
    println!("==================================================");

    Ok(())
}

fn compare_sources() {
    println!("\n==================================================");
    println!("COMPARISON: gRPC vs WebSocket");
    println!("==================================================");
    println!();
    println!("┌─────────────────────────────────────────────────────────────┐");
    println!("│                      L2 VIA gRPC                            │");
    println!("├─────────────────────────────────────────────────────────────┤");
    println!("│ • Lower latency                                             │");
    println!("│ • n_sig_figs parameter for aggregation control              │");
    println!("│ • Best for: HFT, latency-sensitive apps                     │");
    println!("│ • Port: 10000                                               │");
    println!("└─────────────────────────────────────────────────────────────┘");
    println!();
    println!("┌─────────────────────────────────────────────────────────────┐");
    println!("│                    L2 VIA WebSocket                         │");
    println!("├─────────────────────────────────────────────────────────────┤");
    println!("│ • Standard WebSocket (443)                                  │");
    println!("│ • Works in browsers                                         │");
    println!("│ • More subscription types available                         │");
    println!("│ • Best for: Web apps, general use                           │");
    println!("└─────────────────────────────────────────────────────────────┘");
    println!();
}

async fn stream_l2_grpc(endpoint: &str) -> Result<(), Box<dyn std::error::Error>> {
    println!("\n==================================================");
    println!("L2 ORDER BOOK via gRPC");
    println!("==================================================");
    println!();
    println!("gRPC provides lower latency than WebSocket.");
    println!("n_sig_figs controls price aggregation (3-5).");
    println!();

    let update_count = Arc::new(AtomicUsize::new(0));
    let update_count_clone = update_count.clone();

    let mut stream = GRPCStream::new(endpoint)?;

    stream.on_l2_book(move |data| {
        let count = update_count_clone.fetch_add(1, Ordering::SeqCst) + 1;
        if count <= 5 {
            display_l2_book(&data, "grpc", count);
        }
    });

    stream.subscribe_l2_book("BTC", Some(5)).await?;

    println!("Subscribing to BTC L2 book via gRPC (n_sig_figs=5)...");
    println!("------------------------------------------------------------");

    let start = std::time::Instant::now();
    while update_count.load(Ordering::SeqCst) < 5 && start.elapsed() < Duration::from_secs(15) {
        sleep(Duration::from_millis(100)).await;
    }

    stream.stop().await?;
    println!("\nReceived {} L2 updates via gRPC", update_count.load(Ordering::SeqCst));

    Ok(())
}

async fn stream_l2_websocket(endpoint: &str) -> Result<(), Box<dyn std::error::Error>> {
    println!("\n==================================================");
    println!("L2 ORDER BOOK via WebSocket");
    println!("==================================================");

    let update_count = Arc::new(AtomicUsize::new(0));
    let update_count_clone = update_count.clone();

    let mut stream = Stream::new(endpoint)?;

    stream.on_l2_book(move |data| {
        let count = update_count_clone.fetch_add(1, Ordering::SeqCst) + 1;
        if count <= 5 {
            display_l2_book_ws(&data, count);
        }
    });

    stream.subscribe_l2_book("BTC").await?;

    println!("Subscribing to BTC L2 book via WebSocket...");
    println!("------------------------------------------------------------");

    let start = std::time::Instant::now();
    while update_count.load(Ordering::SeqCst) < 5 && start.elapsed() < Duration::from_secs(15) {
        sleep(Duration::from_millis(100)).await;
    }

    stream.stop().await?;
    println!("\nReceived {} L2 updates via WebSocket", update_count.load(Ordering::SeqCst));

    Ok(())
}

fn display_l2_book(data: &serde_json::Value, source: &str, count: usize) {
    let coin = data.get("coin").and_then(|v| v.as_str()).unwrap_or("BTC");
    let bids = data.get("bids").and_then(|v| v.as_array());
    let asks = data.get("asks").and_then(|v| v.as_array());

    println!("\n[{} L2 Book #{} {}]", source.to_uppercase(), count, coin);
    println!("------------------------------------------------------------");

    if let (Some(bids), Some(asks)) = (bids, asks) {
        // Best bid/ask
        if let (Some(best_bid), Some(best_ask)) = (bids.first(), asks.first()) {
            let bid_px = get_price(best_bid);
            let bid_sz = get_size(best_bid);
            let ask_px = get_price(best_ask);
            let ask_sz = get_size(best_ask);
            let spread = ask_px - bid_px;

            println!("  Best Bid: ${:>12,.2f} x {:>10.4}", bid_px, bid_sz);
            println!("  Best Ask: ${:>12,.2f} x {:>10.4}", ask_px, ask_sz);
            println!("  Spread:   ${:>12,.2f} ({:.1} bps)", spread, spread / ((bid_px + ask_px) / 2.0) * 10000.0);
        }
        println!("  Levels:   {} bids, {} asks", bids.len(), asks.len());
    }
}

fn display_l2_book_ws(data: &serde_json::Value, count: usize) {
    let book = data.get("data");
    let coin = data.get("channel").and_then(|v| v.as_str()).unwrap_or("BTC");

    println!("\n[WEBSOCKET L2 Book #{} {}]", count, coin);
    println!("------------------------------------------------------------");

    if let Some(book) = book {
        if let Some(levels) = book.get("levels").and_then(|v| v.as_array()) {
            let bids = levels.get(0).and_then(|v| v.as_array());
            let asks = levels.get(1).and_then(|v| v.as_array());

            if let (Some(bids), Some(asks)) = (bids, asks) {
                if let (Some(best_bid), Some(best_ask)) = (bids.first(), asks.first()) {
                    let bid_px = best_bid.get("px").and_then(|v| v.as_str()).and_then(|s| s.parse::<f64>().ok()).unwrap_or(0.0);
                    let bid_sz = best_bid.get("sz").and_then(|v| v.as_str()).unwrap_or("0");
                    let ask_px = best_ask.get("px").and_then(|v| v.as_str()).and_then(|s| s.parse::<f64>().ok()).unwrap_or(0.0);
                    let ask_sz = best_ask.get("sz").and_then(|v| v.as_str()).unwrap_or("0");
                    let spread = ask_px - bid_px;

                    println!("  Best Bid: ${:>12,.2f} x {}", bid_px, bid_sz);
                    println!("  Best Ask: ${:>12,.2f} x {}", ask_px, ask_sz);
                    println!("  Spread:   ${:>12,.2f}", spread);
                }
                println!("  Levels:   {} bids, {} asks", bids.len(), asks.len());
            }
        }
    }
}

fn get_price(level: &serde_json::Value) -> f64 {
    if let Some(arr) = level.as_array() {
        arr.first().and_then(|v| v.as_str()).and_then(|s| s.parse().ok()).unwrap_or(0.0)
    } else {
        level.get("px").and_then(|v| v.as_str()).and_then(|s| s.parse().ok()).unwrap_or(0.0)
    }
}

fn get_size(level: &serde_json::Value) -> f64 {
    if let Some(arr) = level.as_array() {
        arr.get(1).and_then(|v| v.as_str()).and_then(|s| s.parse().ok()).unwrap_or(0.0)
    } else {
        level.get("sz").and_then(|v| v.as_str()).and_then(|s| s.parse().ok()).unwrap_or(0.0)
    }
}
