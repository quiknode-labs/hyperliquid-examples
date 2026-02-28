//! Cancel by Client Order ID (CLOID) Example
//!
//! Cancel an order using a client-provided order ID instead of the exchange OID.
//! Useful when you track orders by your own IDs.
//!
//! # Usage
//! ```bash
//! export PRIVATE_KEY=0x...
//! cargo run --example cancel_by_cloid
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

    // Note: CLOIDs are hex strings you provide when placing orders
    // This example shows the cancel_by_cloid API

    // Cancel by client order ID
    // let result = sdk.cancel_by_cloid("0x1234567890abcdef...", "BTC").await?;
    // println!("Cancel by cloid result: {:?}", result);

    println!("cancel_by_cloid() cancels orders by your custom client order ID");
    println!("Usage: sdk.cancel_by_cloid(cloid, asset)");

    Ok(())
}
