//! gRPC Streaming Example — High-Performance Real-Time Data
//!
//! Stream trades, orders, L2 book, L4 book, and blocks via gRPC.
//! gRPC provides lower latency than WebSocket for high-frequency trading.
//!
//! gRPC is included with all QuickNode Hyperliquid endpoints — no add-on needed.
//!
//! The SDK:
//! - Connects to port 10000 automatically
//! - Passes token via x-token header
//! - Handles reconnection with exponential backoff
//! - Manages keepalive pings
//!
//! # Usage
//! ```bash
//! export ENDPOINT=https://your-endpoint.hype-mainnet.quiknode.pro/TOKEN
//! cargo run --example stream_grpc
//! ```

use hyperliquid_sdk::{GRPCStream, ConnectionState};
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;
use std::time::Duration;
use tokio::time::sleep;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();

    let endpoint = std::env::var("ENDPOINT").expect("Set ENDPOINT environment variable");

    println!("==================================================");
    println!("gRPC Streaming Examples");
    println!("==================================================");
    println!("Endpoint: {}...", &endpoint[..50.min(endpoint.len())]);
    println!();
    println!("This demo shows all gRPC streaming capabilities:");
    println!("  1. Trades — Real-time executed trades");
    println!("  2. L2 Book — Aggregated order book by price level");
    println!("  3. L4 Book — Individual orders (CRITICAL for trading)");
    println!("  4. Orders — Order lifecycle events");
    println!("  5. Blocks — Block data");
    println!();

    // Example 1: Stream Trades
    stream_trades_example(&endpoint).await?;

    // Example 2: Stream L2 Book
    stream_l2_book_example(&endpoint).await?;

    // Example 3: Stream L4 Book
    stream_l4_book_example(&endpoint).await?;

    // Example 4: Stream Orders
    stream_orders_example(&endpoint).await?;

    // Example 5: Stream Blocks
    stream_blocks_example(&endpoint).await?;

    println!();
    println!("==================================================");
    println!("All examples completed!");
    println!("==================================================");

    Ok(())
}

async fn stream_trades_example(endpoint: &str) -> Result<(), Box<dyn std::error::Error>> {
    println!("\n==================================================");
    println!("EXAMPLE 1: Streaming Trades");
    println!("==================================================");

    let trade_count = Arc::new(AtomicUsize::new(0));
    let trade_count_clone = trade_count.clone();

    let mut stream = GRPCStream::new(endpoint)?;

    stream.on_trade(move |data| {
        let count = trade_count_clone.fetch_add(1, Ordering::SeqCst) + 1;
        let coin = data.get("coin").and_then(|v| v.as_str()).unwrap_or("?");
        let px = data.get("px").and_then(|v| v.as_str()).and_then(|s| s.parse::<f64>().ok()).unwrap_or(0.0);
        let sz = data.get("sz").and_then(|v| v.as_str()).unwrap_or("?");
        let side = if data.get("side").and_then(|v| v.as_str()) == Some("B") { "BUY " } else { "SELL" };
        println!("[TRADE #{}] {} {} {} @ ${:.2}", count, side, sz, coin, px);

        if count >= 5 {
            println!("\nReceived {} trades. Moving to next example...", count);
        }
    });

    stream.subscribe_trades(&["BTC", "ETH"]).await?;

    println!("Subscribing to BTC and ETH trades...");
    println!("------------------------------------------------------------");

    // Wait for trades or timeout
    let start = std::time::Instant::now();
    while trade_count.load(Ordering::SeqCst) < 5 && start.elapsed() < Duration::from_secs(15) {
        sleep(Duration::from_millis(100)).await;
    }

    stream.stop().await?;
    println!("Total trades received: {}", trade_count.load(Ordering::SeqCst));

    Ok(())
}

async fn stream_l2_book_example(endpoint: &str) -> Result<(), Box<dyn std::error::Error>> {
    println!("\n==================================================");
    println!("EXAMPLE 2: Streaming L2 Order Book (Aggregated)");
    println!("==================================================");
    println!();
    println!("L2 book aggregates orders at each price level.");
    println!("Use n_sig_figs to control price aggregation precision.");
    println!();

    let update_count = Arc::new(AtomicUsize::new(0));
    let update_count_clone = update_count.clone();

    let mut stream = GRPCStream::new(endpoint)?;

    stream.on_l2_book(move |data| {
        let count = update_count_clone.fetch_add(1, Ordering::SeqCst) + 1;
        let coin = data.get("coin").and_then(|v| v.as_str()).unwrap_or("BTC");
        let bids = data.get("bids").and_then(|v| v.as_array()).map(|a| a.len()).unwrap_or(0);
        let asks = data.get("asks").and_then(|v| v.as_array()).map(|a| a.len()).unwrap_or(0);

        println!("[L2 #{} {} Book] {} bids, {} asks", count, coin, bids, asks);

        if count >= 3 {
            println!("Received 3 L2 updates. Moving to next example...");
        }
    });

    // n_sig_figs options:
    // 5 = full precision (most levels)
    // 4 = some aggregation
    // 3 = more aggregation (fewer levels, larger sizes)
    stream.subscribe_l2_book("BTC", Some(5)).await?;

    println!("Subscribing to BTC L2 book via gRPC (n_sig_figs=5)...");
    println!("------------------------------------------------------------");

    let start = std::time::Instant::now();
    while update_count.load(Ordering::SeqCst) < 3 && start.elapsed() < Duration::from_secs(15) {
        sleep(Duration::from_millis(100)).await;
    }

    stream.stop().await?;
    println!("Total L2 updates received: {}", update_count.load(Ordering::SeqCst));

    Ok(())
}

async fn stream_l4_book_example(endpoint: &str) -> Result<(), Box<dyn std::error::Error>> {
    println!("\n==================================================");
    println!("EXAMPLE 3: Streaming L4 Order Book (Individual Orders)");
    println!("==================================================");
    println!();
    println!("L4 book shows EVERY individual order in the book.");
    println!("This is critical for market making and order flow analysis.");
    println!();

    let update_count = Arc::new(AtomicUsize::new(0));
    let update_count_clone = update_count.clone();

    let mut stream = GRPCStream::new(endpoint)?;

    stream.on_l4_book(move |data| {
        let count = update_count_clone.fetch_add(1, Ordering::SeqCst) + 1;
        let update_type = data.get("type").and_then(|v| v.as_str()).unwrap_or("unknown");
        let coin = data.get("coin").and_then(|v| v.as_str()).unwrap_or("BTC");
        let bids = data.get("bids").and_then(|v| v.as_array()).map(|a| a.len()).unwrap_or(0);
        let asks = data.get("asks").and_then(|v| v.as_array()).map(|a| a.len()).unwrap_or(0);

        println!("[L4 #{} {} ({})] {} bids, {} asks", count, coin, update_type, bids, asks);

        if count >= 3 {
            println!("Received 3 L4 updates. Moving to next example...");
        }
    });

    stream.subscribe_l4_book("BTC").await?;

    println!("Subscribing to BTC L4 order book (individual orders)...");
    println!("------------------------------------------------------------");

    let start = std::time::Instant::now();
    while update_count.load(Ordering::SeqCst) < 3 && start.elapsed() < Duration::from_secs(15) {
        sleep(Duration::from_millis(100)).await;
    }

    stream.stop().await?;
    println!("Total L4 updates received: {}", update_count.load(Ordering::SeqCst));

    Ok(())
}

async fn stream_orders_example(endpoint: &str) -> Result<(), Box<dyn std::error::Error>> {
    println!("\n==================================================");
    println!("EXAMPLE 4: Streaming Order Events");
    println!("==================================================");
    println!();
    println!("Order events: open, filled, partially_filled, canceled, triggered");
    println!();

    let order_count = Arc::new(AtomicUsize::new(0));
    let order_count_clone = order_count.clone();

    let mut stream = GRPCStream::new(endpoint)?;

    stream.on_order(move |data| {
        let count = order_count_clone.fetch_add(1, Ordering::SeqCst) + 1;
        let coin = data.get("coin").and_then(|v| v.as_str()).unwrap_or("?");
        let status = data.get("status").and_then(|v| v.as_str()).unwrap_or("?");
        let side = if data.get("side").and_then(|v| v.as_str()) == Some("B") { "BUY " } else { "SELL" };
        let px = data.get("px").and_then(|v| v.as_str()).unwrap_or("?");
        let sz = data.get("sz").and_then(|v| v.as_str()).unwrap_or("?");
        let oid = data.get("oid").and_then(|v| v.as_str()).unwrap_or("?");

        println!("[ORDER #{} {}] {} {} {} @ {} (oid: {})", count, status.to_uppercase(), side, sz, coin, px, oid);

        if count >= 5 {
            println!("\nReceived {} order events. Moving to next example...", count);
        }
    });

    stream.subscribe_orders(&["BTC", "ETH"]).await?;

    println!("Subscribing to BTC and ETH order events...");
    println!("------------------------------------------------------------");

    let start = std::time::Instant::now();
    while order_count.load(Ordering::SeqCst) < 5 && start.elapsed() < Duration::from_secs(15) {
        sleep(Duration::from_millis(100)).await;
    }

    stream.stop().await?;
    println!("Total order events received: {}", order_count.load(Ordering::SeqCst));

    Ok(())
}

async fn stream_blocks_example(endpoint: &str) -> Result<(), Box<dyn std::error::Error>> {
    println!("\n==================================================");
    println!("EXAMPLE 5: Streaming Blocks");
    println!("==================================================");

    let block_count = Arc::new(AtomicUsize::new(0));
    let block_count_clone = block_count.clone();

    let mut stream = GRPCStream::new(endpoint)?;

    stream.on_block(move |data| {
        let count = block_count_clone.fetch_add(1, Ordering::SeqCst) + 1;
        let abci_block = data.get("abci_block");
        let block_time = abci_block.and_then(|b| b.get("time")).and_then(|v| v.as_str()).unwrap_or("?");
        let bundles = abci_block
            .and_then(|b| b.get("signed_action_bundles"))
            .and_then(|v| v.as_array())
            .map(|a| a.len())
            .unwrap_or(0);

        println!("[BLOCK #{}] @ {} ({} bundles)", count, block_time, bundles);

        if count >= 3 {
            println!("\nReceived {} blocks. Demo complete!", count);
        }
    });

    stream.subscribe_blocks().await?;

    println!("Subscribing to blocks...");
    println!("------------------------------------------------------------");

    let start = std::time::Instant::now();
    while block_count.load(Ordering::SeqCst) < 3 && start.elapsed() < Duration::from_secs(30) {
        sleep(Duration::from_millis(100)).await;
    }

    stream.stop().await?;
    println!("Total blocks received: {}", block_count.load(Ordering::SeqCst));

    Ok(())
}
