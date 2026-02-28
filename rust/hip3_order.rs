//! HIP-3 Market Order Example
//!
//! Trade on HIP-3 markets (community perps like Hypersea).
//! Same API as regular markets, just use "dex:symbol" format.
//!
//! # Usage
//! ```bash
//! export PRIVATE_KEY=0x...
//! cargo run --example hip3_order
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

    // List HIP-3 DEXes
    let dexes = sdk.dexes().await?;
    println!("Available HIP-3 DEXes:");
    if let Some(arr) = dexes.as_array() {
        for dex in arr.iter().take(5) {
            if let Some(name) = dex.get("name").and_then(|v| v.as_str()) {
                println!("  {}", name);
            }
        }
    }

    // Trade on a HIP-3 market
    // Format: "dex:SYMBOL"
    // let order = sdk.market_buy("xyz:SILVER").await.notional(11.0).await?;
    // println!("HIP-3 order: {:?}", order);

    println!("\nHIP-3 markets use 'dex:SYMBOL' format");
    println!("Example: sdk.market_buy(\"xyz:SILVER\").await.notional(11.0).await?");

    Ok(())
}
