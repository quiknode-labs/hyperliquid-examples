//! Market Data Example
//!
//! Shows how to query market metadata, prices, order book, and recent trades.
//!
//! The SDK handles all Info API methods automatically.
//!
//! # Usage
//! ```bash
//! export ENDPOINT=https://your-endpoint.hype-mainnet.quiknode.pro/TOKEN
//! cargo run --example info_market_data
//! ```

use hyperliquid_sdk::HyperliquidSDK;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();

    let endpoint = std::env::var("ENDPOINT").expect("Set ENDPOINT environment variable");

    let sdk = HyperliquidSDK::new()
        .endpoint(&endpoint)
        .build()
        .await?;

    println!("==================================================");
    println!("Market Data (Info API)");
    println!("==================================================");

    // Exchange metadata
    println!("\n1. Exchange Metadata:");
    match sdk.info().meta().await {
        Ok(meta) => {
            if let Some(universe) = meta.get("universe").and_then(|v| v.as_array()) {
                println!("   Perp Markets: {}", universe.len());
                for asset in universe.iter().take(5) {
                    let name = asset.get("name").and_then(|v| v.as_str()).unwrap_or("?");
                    let max_lev = asset.get("maxLeverage").and_then(|v| v.as_u64()).unwrap_or(0);
                    println!("   - {}: max leverage {}x", name, max_lev);
                }
            }
        }
        Err(e) => println!("   (meta not available: {})", e),
    }

    // Spot metadata
    println!("\n2. Spot Metadata:");
    match sdk.info().spot_meta().await {
        Ok(spot) => {
            if let Some(tokens) = spot.get("tokens").and_then(|v| v.as_array()) {
                println!("   Spot Tokens: {}", tokens.len());
            }
        }
        Err(e) => println!("   (spot_meta not available: {})", e),
    }

    // Exchange status
    println!("\n3. Exchange Status:");
    match sdk.info().exchange_status().await {
        Ok(status) => println!("   {:?}", status),
        Err(e) => println!("   (exchange_status not available: {})", e),
    }

    // All mid prices
    println!("\n4. Mid Prices:");
    match sdk.info().all_mids().await {
        Ok(mids) => {
            if let Some(btc) = mids.get("BTC").and_then(|v| v.as_str()).and_then(|s| s.parse::<f64>().ok()) {
                println!("   BTC: ${:.2}", btc);
            }
            if let Some(eth) = mids.get("ETH").and_then(|v| v.as_str()).and_then(|s| s.parse::<f64>().ok()) {
                println!("   ETH: ${:.2}", eth);
            }
        }
        Err(e) => println!("   (allMids not available: {})", e),
    }

    // Order book
    println!("\n5. Order Book (BTC):");
    match sdk.info().l2_book("BTC").await {
        Ok(book) => {
            if let Some(levels) = book.get("levels").and_then(|v| v.as_array()) {
                if levels.len() >= 2 {
                    if let (Some(bids), Some(asks)) = (levels[0].as_array(), levels[1].as_array()) {
                        if let (Some(best_bid), Some(best_ask)) = (bids.first(), asks.first()) {
                            let bid_px = best_bid.get("px").and_then(|v| v.as_str()).and_then(|s| s.parse::<f64>().ok()).unwrap_or(0.0);
                            let ask_px = best_ask.get("px").and_then(|v| v.as_str()).and_then(|s| s.parse::<f64>().ok()).unwrap_or(0.0);
                            let spread = ask_px - bid_px;
                            println!("   Best Bid: ${:.2}", bid_px);
                            println!("   Best Ask: ${:.2}", ask_px);
                            println!("   Spread: ${:.2}", spread);
                        }
                    }
                }
            }
        }
        Err(e) => println!("   (l2_book not available: {})", e),
    }

    // Recent trades
    println!("\n6. Recent Trades (BTC):");
    match sdk.info().recent_trades("BTC").await {
        Ok(trades) => {
            if let Some(arr) = trades.as_array() {
                for t in arr.iter().take(3) {
                    let side = if t.get("side").and_then(|v| v.as_str()) == Some("B") { "BUY" } else { "SELL" };
                    let sz = t.get("sz").and_then(|v| v.as_str()).unwrap_or("?");
                    let px = t.get("px").and_then(|v| v.as_str()).and_then(|s| s.parse::<f64>().ok()).unwrap_or(0.0);
                    println!("   {} {} @ ${:.2}", side, sz, px);
                }
            }
        }
        Err(e) => println!("   (recent_trades not available: {})", e),
    }

    println!("\n==================================================");
    println!("Done!");

    Ok(())
}
