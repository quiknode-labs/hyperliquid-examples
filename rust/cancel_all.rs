//! Cancel All Orders Example
//!
//! Cancel all open orders, or all orders for a specific asset.
//!
//! # Usage
//! ```bash
//! export PRIVATE_KEY=0x...
//! cargo run --example cancel_all
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

    // Check open orders first
    let orders = sdk.open_orders().await?;
    if let Some(arr) = orders.as_array() {
        println!("Open orders: {}", arr.len());
    }

    // Cancel all orders
    let result = sdk.cancel_all(None).await?;
    println!("Cancel all result: {:?}", result);

    // Or cancel just BTC orders:
    // let result = sdk.cancel_all(Some("BTC")).await?;
    // println!("Cancel BTC orders: {:?}", result);

    Ok(())
}
