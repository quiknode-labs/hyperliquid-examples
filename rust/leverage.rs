//! Leverage Example
//!
//! Update leverage for a position.
//!
//! # Usage
//! ```bash
//! export PRIVATE_KEY=0x...
//! cargo run --example leverage
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

    // Update leverage for BTC to 10x cross margin
    let result = sdk.update_leverage("BTC", 10, true).await?;
    println!("Update leverage result: {:?}", result);

    // Update leverage for ETH to 5x isolated margin
    // let result = sdk.update_leverage("ETH", 5, false).await?;
    // println!("Update leverage result: {:?}", result);

    println!("\nLeverage methods available:");
    println!("  sdk.update_leverage(asset, leverage, is_cross)");

    Ok(())
}
