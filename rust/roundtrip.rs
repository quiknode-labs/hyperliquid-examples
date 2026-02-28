//! Round Trip Example
//!
//! Complete trade cycle: buy then sell to end up flat.
//!
//! # Usage
//! ```bash
//! export PRIVATE_KEY=0x...
//! cargo run --example roundtrip
//! ```

use hyperliquid_sdk::HyperliquidSDK;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();

    let endpoint = std::env::var("ENDPOINT").ok();

    let mut builder = HyperliquidSDK::new();
    if let Some(ep) = endpoint {
        builder = builder.endpoint(ep);
    }

    let sdk = builder.build().await?;

    println!("SDK initialized for address: {:?}", sdk.address());

    // Buy $11 worth of BTC
    println!("Buying BTC...");
    let buy = sdk.market_buy("BTC").await.notional(11.0).await?;
    let filled_size = buy.filled_size.unwrap_or(buy.size.unwrap_or(0.0));
    println!("  Bought: {} BTC", filled_size);
    println!("  Status: {}", buy.status);

    // Sell the same amount
    println!("Selling BTC...");
    let sell = sdk.market_sell("BTC").await.size(filled_size).await?;
    let sold_size = sell.filled_size.unwrap_or(sell.size.unwrap_or(0.0));
    println!("  Sold: {} BTC", sold_size);
    println!("  Status: {}", sell.status);

    println!("Done! Position should be flat.");

    Ok(())
}
