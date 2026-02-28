//! Close Position Example
//!
//! Close an open position completely. The SDK figures out the size and direction.
//!
//! # Usage
//! ```bash
//! export PRIVATE_KEY=0x...
//! cargo run --example close_position
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

    // Close BTC position (if any)
    // The SDK queries your position and builds the counter-order automatically
    match sdk.close_position("BTC").await {
        Ok(result) => println!("Closed position: {:?}", result),
        Err(e) => println!("No position to close or error: {}", e),
    }

    Ok(())
}
