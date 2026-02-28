//! HyperCore Block Data Example
//!
//! Shows how to get real-time trades, orders, and block data via the HyperCore API.
//!
//! This is the alternative to Info methods (allMids, l2Book, recentTrades) that
//! are not available on QuickNode endpoints.
//!
//! # Usage
//! ```bash
//! export ENDPOINT=https://your-endpoint.hype-mainnet.quiknode.pro/TOKEN
//! cargo run --example hypercore_blocks
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
    println!("HyperCore Block Data");
    println!("==================================================");

    // Latest block number
    println!("\n1. Latest Block:");
    let block_num = sdk.core().latest_block_number().await?;
    println!("   Block #{}", block_num);

    // Recent trades
    println!("\n2. Recent Trades (all coins):");
    let trades = sdk.core().latest_trades(5, None).await?;
    if let Some(arr) = trades.as_array() {
        for t in arr.iter().take(5) {
            let side = if t.get("side").and_then(|v| v.as_str()) == Some("B") { "BUY" } else { "SELL" };
            let sz = t.get("sz").and_then(|v| v.as_str()).unwrap_or("?");
            let coin = t.get("coin").and_then(|v| v.as_str()).unwrap_or("?");
            let px = t.get("px").and_then(|v| v.as_str()).unwrap_or("?");
            println!("   {} {} {} @ ${}", side, sz, coin, px);
        }
    }

    // Recent BTC trades only
    println!("\n3. BTC Trades:");
    let btc_trades = sdk.core().latest_trades(10, Some("BTC")).await?;
    if let Some(arr) = btc_trades.as_array() {
        if arr.is_empty() {
            println!("   No BTC trades in recent blocks");
        } else {
            for t in arr.iter().take(3) {
                let side = if t.get("side").and_then(|v| v.as_str()) == Some("B") { "BUY" } else { "SELL" };
                let sz = t.get("sz").and_then(|v| v.as_str()).unwrap_or("?");
                let px = t.get("px").and_then(|v| v.as_str()).unwrap_or("?");
                println!("   {} {} @ ${}", side, sz, px);
            }
        }
    }

    // Get a specific block
    println!("\n4. Get Block Data:");
    let block = sdk.core().get_block(block_num - 1).await?;
    println!("   Block #{}", block_num - 1);
    if let Some(time) = block.get("block_time").and_then(|v| v.as_str()) {
        println!("   Time: {}", time);
    }
    if let Some(events) = block.get("events").and_then(|v| v.as_array()) {
        println!("   Events: {}", events.len());
    }

    // Get batch of blocks
    println!("\n5. Batch Blocks:");
    let blocks = sdk.core().get_batch_blocks(block_num - 5, block_num - 1).await?;
    if let Some(arr) = blocks.get("blocks").and_then(|v| v.as_array()) {
        println!("   Retrieved {} blocks", arr.len());
    }

    println!("\n==================================================");
    println!("Done!");

    Ok(())
}
