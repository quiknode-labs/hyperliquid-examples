//! Order Book Streaming Example — L2 and L4 Order Books via gRPC
//!
//! This example demonstrates how to stream order book data via gRPC:
//! - L2 Book: Aggregated by price level (total size and order count per price)
//! - L4 Book: Individual orders with order IDs
//!
//! Note: L2/L4 order books are only available via gRPC on QuickNode.
//!       WebSocket streaming provides book_updates (incremental deltas) instead.
//!
//! Use cases:
//! - L2 Book: Market depth, spread monitoring, analytics dashboards
//! - L4 Book: HFT, quant trading, market making, order flow analysis
//!
//! # Usage
//! ```bash
//! export ENDPOINT=https://your-endpoint.hype-mainnet.quiknode.pro/TOKEN
//! cargo run --example stream_orderbook
//! ```

use hyperliquid_sdk::GRPCStream;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;
use std::time::Duration;
use tokio::time::sleep;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();

    let endpoint = std::env::var("ENDPOINT").expect("Set ENDPOINT environment variable");

    println!("==================================================");
    println!("Order Book Streaming Examples (gRPC)");
    println!("==================================================");
    println!("Endpoint: {}...", &endpoint[..50.min(endpoint.len())]);

    // Show comparison
    comparison();

    // Run L2 example
    stream_l2_grpc(&endpoint).await?;

    // Run L4 example (CRITICAL)
    stream_l4_book(&endpoint).await?;

    println!();
    println!("==================================================");
    println!("All examples completed!");
    println!("==================================================");

    Ok(())
}

fn comparison() {
    println!("\n==================================================");
    println!("L2 vs L4 ORDER BOOK COMPARISON");
    println!("==================================================");
    println!();
    println!("┌─────────────────────────────────────────────────────────────┐");
    println!("│                    L2 ORDER BOOK                            │");
    println!("├─────────────────────────────────────────────────────────────┤");
    println!("│ • Aggregated by price level                                 │");
    println!("│ • Shows total size at each price                            │");
    println!("│ • Available via gRPC (StreamL2Book)                         │");
    println!("│ • Lower bandwidth                                           │");
    println!("│ • Good for: Price monitoring, simple trading                │");
    println!("├─────────────────────────────────────────────────────────────┤");
    println!("│ Example:                                                    │");
    println!("│   Price: $95,000.00 | Total Size: 10.5 BTC                  │");
    println!("│   (You don't know how many orders or their sizes)           │");
    println!("└─────────────────────────────────────────────────────────────┘");
    println!();
    println!("┌─────────────────────────────────────────────────────────────┐");
    println!("│                    L4 ORDER BOOK                            │");
    println!("├─────────────────────────────────────────────────────────────┤");
    println!("│ • Individual orders with order IDs                          │");
    println!("│ • Shows each order separately                               │");
    println!("│ • Available via gRPC (StreamL4Book)                         │");
    println!("│ • Higher bandwidth but more detail                          │");
    println!("│ • Good for: Market making, HFT, order flow analysis         │");
    println!("├─────────────────────────────────────────────────────────────┤");
    println!("│ Example:                                                    │");
    println!("│   Price: $95,000.00                                         │");
    println!("│     └─ Order 1: 5.0 BTC (oid: abc123...)                    │");
    println!("│     └─ Order 2: 3.0 BTC (oid: def456...)                    │");
    println!("│     └─ Order 3: 2.5 BTC (oid: ghi789...)                    │");
    println!("│   (You see every order and can track queue position)        │");
    println!("└─────────────────────────────────────────────────────────────┘");
    println!();
    println!("Note: For incremental book changes (deltas), use WebSocket:");
    println!("  stream.subscribe_book_updates(coins)");
    println!();
}

async fn stream_l2_grpc(endpoint: &str) -> Result<(), Box<dyn std::error::Error>> {
    println!("\n==================================================");
    println!("L2 ORDER BOOK via gRPC");
    println!("==================================================");
    println!();
    println!("L2 book aggregates all orders at each price level.");
    println!("n_sig_figs controls aggregation precision.");
    println!();

    let update_count = Arc::new(AtomicUsize::new(0));
    let update_count_clone = update_count.clone();

    let mut stream = GRPCStream::new(endpoint)?;

    stream.on_l2_book(move |data| {
        let count = update_count_clone.fetch_add(1, Ordering::SeqCst) + 1;
        if count <= 3 {
            display_l2(&data, count);
        }
    });

    stream.subscribe_l2_book("BTC", Some(5)).await?;

    println!("Subscribing to BTC L2 book via gRPC...");
    println!("------------------------------------------------------------");

    let start = std::time::Instant::now();
    while update_count.load(Ordering::SeqCst) < 3 && start.elapsed() < Duration::from_secs(15) {
        sleep(Duration::from_millis(100)).await;
    }

    stream.stop().await?;
    println!("\nReceived {} L2 updates via gRPC", update_count.load(Ordering::SeqCst));

    Ok(())
}

async fn stream_l4_book(endpoint: &str) -> Result<(), Box<dyn std::error::Error>> {
    println!("\n==================================================");
    println!("L4 ORDER BOOK via gRPC (Individual Orders)");
    println!("==================================================");
    println!();
    println!("L4 book shows EVERY individual order with order ID.");
    println!("This is CRITICAL for market making and order flow analysis.");
    println!();
    println!("Use cases:");
    println!("  - See exact queue position");
    println!("  - Detect large orders / icebergs");
    println!("  - Know exactly what you're crossing");
    println!("  - Analyze order flow");
    println!();

    let update_count = Arc::new(AtomicUsize::new(0));
    let update_count_clone = update_count.clone();

    let mut stream = GRPCStream::new(endpoint)?;

    stream.on_l4_book(move |data| {
        let count = update_count_clone.fetch_add(1, Ordering::SeqCst) + 1;
        if count <= 3 {
            display_l4(&data, count);
        }
    });

    stream.subscribe_l4_book("BTC").await?;

    println!("Subscribing to BTC L4 book via gRPC...");
    println!("------------------------------------------------------------");

    let start = std::time::Instant::now();
    while update_count.load(Ordering::SeqCst) < 3 && start.elapsed() < Duration::from_secs(15) {
        sleep(Duration::from_millis(100)).await;
    }

    stream.stop().await?;
    println!("\nReceived {} L4 updates", update_count.load(Ordering::SeqCst));

    Ok(())
}

fn display_l2(data: &serde_json::Value, count: usize) {
    let coin = data.get("coin").and_then(|v| v.as_str()).unwrap_or("BTC");
    let bids = data.get("bids").and_then(|v| v.as_array());
    let asks = data.get("asks").and_then(|v| v.as_array());

    println!("\n{} L2 Order Book (#{}) ", coin, count);
    println!("────────────────────────────────────────");

    if let (Some(bids), Some(asks)) = (bids, asks) {
        if let (Some(best_bid), Some(best_ask)) = (bids.first(), asks.first()) {
            let bid_px = get_arr_value(best_bid, 0);
            let bid_sz = get_arr_value(best_bid, 1);
            let ask_px = get_arr_value(best_ask, 0);
            let ask_sz = get_arr_value(best_ask, 1);
            let spread = ask_px - bid_px;
            let spread_bps = if bid_px > 0.0 { spread / ((bid_px + ask_px) / 2.0) * 10000.0 } else { 0.0 };

            println!("  Best Bid: ${:>12,.2f} x {:>10.4}", bid_px, bid_sz);
            println!("  Best Ask: ${:>12,.2f} x {:>10.4}", ask_px, ask_sz);
            println!("  Spread:   ${:>12,.2f} ({:.2} bps)", spread, spread_bps);
        }
        println!("  Levels:   {} bids, {} asks", bids.len(), asks.len());
    }
}

fn display_l4(data: &serde_json::Value, count: usize) {
    let coin = data.get("coin").and_then(|v| v.as_str()).unwrap_or("BTC");
    let bids = data.get("bids").and_then(|v| v.as_array());
    let asks = data.get("asks").and_then(|v| v.as_array());

    println!("\n{} L4 Order Book (Individual Orders) (#{}) ", coin, count);
    println!("============================================================");

    if let Some(asks) = asks {
        println!("\nASKS (top 5 price levels):");
        for ask in asks.iter().take(5).rev() {
            if let Some(arr) = ask.as_array() {
                if arr.len() >= 3 {
                    let px = arr[0].as_str().and_then(|s| s.parse::<f64>().ok()).unwrap_or(0.0);
                    let sz = arr[1].as_str().unwrap_or("?");
                    let oid = arr[2].as_str().map(|s| if s.len() > 8 { &s[..8] } else { s }).unwrap_or("?");
                    println!("  ${:>12,.2f} | {:>10} | oid: {}...", px, sz, oid);
                }
            }
        }
    }

    println!("  ────────────────────────────────────────────────────────");
    println!("                         SPREAD");
    println!("  ────────────────────────────────────────────────────────");

    if let Some(bids) = bids {
        println!("\nBIDS (top 5 price levels):");
        for bid in bids.iter().take(5) {
            if let Some(arr) = bid.as_array() {
                if arr.len() >= 3 {
                    let px = arr[0].as_str().and_then(|s| s.parse::<f64>().ok()).unwrap_or(0.0);
                    let sz = arr[1].as_str().unwrap_or("?");
                    let oid = arr[2].as_str().map(|s| if s.len() > 8 { &s[..8] } else { s }).unwrap_or("?");
                    println!("  ${:>12,.2f} | {:>10} | oid: {}...", px, sz, oid);
                }
            }
        }

        let bid_count = bids.len();
        let ask_count = asks.map(|a| a.len()).unwrap_or(0);
        println!("\nTotal: {} bid orders, {} ask orders", bid_count, ask_count);
    }
}

fn get_arr_value(v: &serde_json::Value, idx: usize) -> f64 {
    v.as_array()
        .and_then(|a| a.get(idx))
        .and_then(|v| v.as_str())
        .and_then(|s| s.parse().ok())
        .unwrap_or(0.0)
}
