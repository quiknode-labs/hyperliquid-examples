//! L4 Order Book Streaming via gRPC — Individual Orders with Order IDs
//!
//! L4 order book is CRITICAL for:
//! - Market making: Know your exact queue position
//! - Order flow analysis: Detect large orders, icebergs
//! - Optimal execution: See exactly what you're crossing
//! - HFT: Lower latency than WebSocket
//!
//! This example shows how to:
//! 1. Stream L4 order book updates
//! 2. Track individual orders
//! 3. Calculate depth and queue position
//!
//! # Usage
//! ```bash
//! export ENDPOINT=https://your-endpoint.hype-mainnet.quiknode.pro/TOKEN
//! cargo run --example stream_l4_book
//! ```

use hyperliquid_sdk::GRPCStream;
use std::collections::HashMap;
use std::sync::{Arc, RwLock};
use std::sync::atomic::{AtomicUsize, Ordering};
use std::time::Duration;
use tokio::time::sleep;

/// Track L4 order book state
struct L4BookManager {
    coin: String,
    bids: HashMap<String, serde_json::Value>,
    asks: HashMap<String, serde_json::Value>,
    update_count: usize,
}

impl L4BookManager {
    fn new(coin: &str) -> Self {
        Self {
            coin: coin.to_string(),
            bids: HashMap::new(),
            asks: HashMap::new(),
            update_count: 0,
        }
    }

    fn process_update(&mut self, data: &serde_json::Value) {
        self.update_count += 1;

        // Process bids
        if let Some(bids) = data.get("bids").and_then(|v| v.as_array()) {
            for bid in bids {
                self.process_level(bid, true);
            }
        }

        // Process asks
        if let Some(asks) = data.get("asks").and_then(|v| v.as_array()) {
            for ask in asks {
                self.process_level(ask, false);
            }
        }
    }

    fn process_level(&mut self, level: &serde_json::Value, is_bid: bool) {
        let book = if is_bid { &mut self.bids } else { &mut self.asks };

        if let Some(arr) = level.as_array() {
            if arr.len() >= 3 {
                // Format: [price, size, order_id]
                let sz = arr[1].as_str().and_then(|s| s.parse::<f64>().ok()).unwrap_or(0.0);
                let oid = arr[2].as_str().unwrap_or("").to_string();
                if sz == 0.0 {
                    book.remove(&oid);
                } else {
                    book.insert(oid, level.clone());
                }
            }
        }
    }

    fn display(&self, levels: usize) {
        println!("\n{'='repeat 60}");
        println!("{} L4 ORDER BOOK (Update #{})", self.coin, self.update_count);
        println!("{'='repeat 60}");

        // Group orders by price for display
        let mut ask_by_price: HashMap<String, Vec<&serde_json::Value>> = HashMap::new();
        for order in self.asks.values() {
            if let Some(arr) = order.as_array() {
                if let Some(px) = arr.first().and_then(|v| v.as_str()) {
                    ask_by_price.entry(px.to_string()).or_default().push(order);
                }
            }
        }

        let mut bid_by_price: HashMap<String, Vec<&serde_json::Value>> = HashMap::new();
        for order in self.bids.values() {
            if let Some(arr) = order.as_array() {
                if let Some(px) = arr.first().and_then(|v| v.as_str()) {
                    bid_by_price.entry(px.to_string()).or_default().push(order);
                }
            }
        }

        // Display asks
        println!("\n ASKS:");
        let mut ask_prices: Vec<_> = ask_by_price.keys().collect();
        ask_prices.sort_by(|a, b| {
            let pa: f64 = a.parse().unwrap_or(0.0);
            let pb: f64 = b.parse().unwrap_or(0.0);
            pa.partial_cmp(&pb).unwrap()
        });
        for px in ask_prices.iter().take(levels).rev() {
            if let Some(orders) = ask_by_price.get(*px) {
                let total_sz: f64 = orders.iter()
                    .filter_map(|o| o.as_array())
                    .filter_map(|a| a.get(1).and_then(|v| v.as_str()).and_then(|s| s.parse().ok()))
                    .sum();
                let px_f: f64 = px.parse().unwrap_or(0.0);
                println!("  ${:>12,.2f} │ {:>10.4f} │ {:>2} orders", px_f, total_sz, orders.len());
            }
        }

        println!("\n  ────────────────────────────────────────────");
        println!("  SPREAD");
        println!("  ────────────────────────────────────────────\n");

        // Display bids
        println!(" BIDS:");
        let mut bid_prices: Vec<_> = bid_by_price.keys().collect();
        bid_prices.sort_by(|a, b| {
            let pa: f64 = a.parse().unwrap_or(0.0);
            let pb: f64 = b.parse().unwrap_or(0.0);
            pb.partial_cmp(&pa).unwrap()
        });
        for px in bid_prices.iter().take(levels) {
            if let Some(orders) = bid_by_price.get(*px) {
                let total_sz: f64 = orders.iter()
                    .filter_map(|o| o.as_array())
                    .filter_map(|a| a.get(1).and_then(|v| v.as_str()).and_then(|s| s.parse().ok()))
                    .sum();
                let px_f: f64 = px.parse().unwrap_or(0.0);
                println!("  ${:>12,.2f} │ {:>10.4f} │ {:>2} orders", px_f, total_sz, orders.len());
            }
        }

        println!("\n SUMMARY:");
        println!("  Total Bid Orders: {:>6}", self.bids.len());
        println!("  Total Ask Orders: {:>6}", self.asks.len());
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();

    let endpoint = std::env::var("ENDPOINT").expect("Set ENDPOINT environment variable");

    println!("==================================================");
    println!("L4 ORDER BOOK STREAMING (gRPC)");
    println!("==================================================");
    println!("Endpoint: {}...", &endpoint[..50.min(endpoint.len())]);
    println!();
    println!("L4 book shows individual orders with order IDs.");
    println!("This is essential for:");
    println!("  - Market making (queue position)");
    println!("  - Order flow analysis (large orders)");
    println!("  - Optimal execution (what you're crossing)");
    println!();

    let book = Arc::new(RwLock::new(L4BookManager::new("BTC")));
    let book_clone = book.clone();
    let update_count = Arc::new(AtomicUsize::new(0));
    let update_count_clone = update_count.clone();

    let mut stream = GRPCStream::new(&endpoint)?;

    stream.on_l4_book(move |data| {
        let count = update_count_clone.fetch_add(1, Ordering::SeqCst) + 1;

        if let Ok(mut b) = book_clone.write() {
            b.process_update(&data);

            // Display every update for first 5, then every 10th
            if count <= 5 || count % 10 == 0 {
                b.display(3);
            }
        }

        if count >= 30 {
            println!("\nReceived {} updates. Stopping...", count);
        }
    });

    println!("Subscribing to BTC L4 order book...");
    stream.subscribe_l4_book("BTC").await?;

    println!("------------------------------------------------------------");
    println!("Streaming L4 book... (Ctrl+C to stop)");
    println!();

    // Run for 60 seconds or until we have 30 updates
    let start = std::time::Instant::now();
    while update_count.load(Ordering::SeqCst) < 30 && start.elapsed() < Duration::from_secs(60) {
        sleep(Duration::from_millis(500)).await;
    }

    stream.stop().await?;

    if let Ok(b) = book.read() {
        println!();
        println!("==================================================");
        println!("L4 BOOK STREAMING COMPLETE");
        println!("==================================================");
        println!("Total updates received: {}", b.update_count);
        println!("Final bid orders: {}", b.bids.len());
        println!("Final ask orders: {}", b.asks.len());
    }

    Ok(())
}
