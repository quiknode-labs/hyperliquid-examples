//! WebSocket Streaming Example
//!
//! Demonstrates real-time streaming of trades and other market data.
//!
//! # Usage
//! ```bash
//! export ENDPOINT=https://your-endpoint.hype-mainnet.quiknode.pro/TOKEN
//! cargo run --example stream_trades
//! ```

use hyperliquid_sdk::Stream;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;
use std::time::Duration;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();

    let endpoint = std::env::var("ENDPOINT").ok();

    // Create stream with callbacks
    let trade_count = Arc::new(AtomicUsize::new(0));
    let trade_count_cb = trade_count.clone();

    let mut stream = Stream::new(endpoint)
        .on_open(|| {
            println!("✓ WebSocket connected!");
        })
        .on_error(|e| {
            eprintln!("✗ WebSocket error: {}", e);
        })
        .on_close(|| {
            println!("WebSocket closed");
        })
        .on_state_change(|state| {
            println!("State changed: {:?}", state);
        })
        .on_reconnect(|attempt| {
            println!("Reconnecting... attempt {}", attempt);
        });

    // ─────────────────────────────────────────────────────────────────────────
    // Subscribe to Trades
    // ─────────────────────────────────────────────────────────────────────────

    println!("Subscribing to BTC and ETH trades...");
    let _trade_sub = stream.trades(&["BTC", "ETH"], move |data| {
        trade_count_cb.fetch_add(1, Ordering::SeqCst);

        // Parse trade data
        if let Some(trades) = data.get("data").and_then(|d| d.as_array()) {
            for trade in trades {
                let coin = trade.get("coin").and_then(|c| c.as_str()).unwrap_or("?");
                let px = trade.get("px").and_then(|p| p.as_str()).unwrap_or("?");
                let sz = trade.get("sz").and_then(|s| s.as_str()).unwrap_or("?");
                let side = trade.get("side").and_then(|s| s.as_str()).unwrap_or("?");

                println!(
                    "[TRADE] {} {} {} @ {} ({})",
                    coin,
                    side.to_uppercase(),
                    sz,
                    px,
                    if side == "B" { "buy" } else { "sell" }
                );
            }
        }
    });

    // ─────────────────────────────────────────────────────────────────────────
    // Subscribe to L2 Order Book
    // ─────────────────────────────────────────────────────────────────────────

    println!("Subscribing to BTC L2 order book...");
    let _book_sub = stream.l2_book("BTC", |data| {
        if let Some(levels) = data.get("data").and_then(|d| d.get("levels")) {
            // Get best bid and ask
            let bids = levels.get(0).and_then(|b| b.as_array());
            let asks = levels.get(1).and_then(|a| a.as_array());

            if let (Some(bids), Some(asks)) = (bids, asks) {
                if let (Some(best_bid), Some(best_ask)) = (bids.first(), asks.first()) {
                    let bid_px = best_bid.get("px").and_then(|p| p.as_str()).unwrap_or("?");
                    let ask_px = best_ask.get("px").and_then(|p| p.as_str()).unwrap_or("?");
                    println!("[BOOK] BTC bid: {} | ask: {}", bid_px, ask_px);
                }
            }
        }
    });

    // ─────────────────────────────────────────────────────────────────────────
    // Subscribe to All Mid Prices
    // ─────────────────────────────────────────────────────────────────────────

    println!("Subscribing to all mid prices...");
    let _mids_sub = stream.all_mids(|data| {
        if let Some(mids) = data.get("data").and_then(|d| d.get("mids")) {
            if let Some(btc_mid) = mids.get("BTC").and_then(|m| m.as_str()) {
                println!("[MIDS] BTC: {}", btc_mid);
            }
        }
    });

    // ─────────────────────────────────────────────────────────────────────────
    // Start Streaming
    // ─────────────────────────────────────────────────────────────────────────

    println!("\nStarting stream (will run for 30 seconds)...\n");
    stream.start()?;

    // Run for 30 seconds
    tokio::time::sleep(Duration::from_secs(30)).await;

    // Stop the stream
    stream.stop();

    println!(
        "\n\nTotal trades received: {}",
        trade_count.load(Ordering::SeqCst)
    );

    Ok(())
}
