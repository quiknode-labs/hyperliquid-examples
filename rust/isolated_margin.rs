//! Isolated Margin Example
//!
//! Add or remove margin from an isolated position.
//!
//! # Usage
//! ```bash
//! export PRIVATE_KEY=0x...
//! cargo run --example isolated_margin
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

    // Add $100 margin to BTC long position (is_buy=true for long)
    // let result = sdk.update_isolated_margin("BTC", 100.0, true).await?;
    // println!("Add margin result: {:?}", result);

    // Remove $50 margin from ETH short position (is_buy=false for short)
    // let result = sdk.update_isolated_margin("ETH", -50.0, false).await?;
    // println!("Remove margin result: {:?}", result);

    // Top up isolated-only margin (special maintenance mode)
    // let result = sdk.top_up_isolated_only_margin("BTC", 100.0).await?;
    // println!("Top up isolated-only margin result: {:?}", result);

    println!("\nIsolated margin methods available:");
    println!("  sdk.update_isolated_margin(asset, amount, is_buy)");
    println!("  sdk.top_up_isolated_only_margin(asset, amount)");

    Ok(())
}
