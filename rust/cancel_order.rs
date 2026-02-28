//! Cancel Order Example
//!
//! Cancel a specific order by OID.
//!
//! # Usage
//! ```bash
//! export PRIVATE_KEY=0x...
//! cargo run --example cancel_order
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

    // Get open orders
    let orders = sdk.open_orders().await?;
    if let Some(arr) = orders.as_array() {
        println!("Open orders: {}", arr.len());

        // Cancel first order if any
        if let Some(order) = arr.first() {
            if let (Some(oid), Some(coin)) = (
                order.get("oid").and_then(|v| v.as_u64()),
                order.get("coin").and_then(|v| v.as_str()),
            ) {
                println!("Canceling order {} for {}", oid, coin);
                let result = sdk.cancel(oid, coin).await?;
                println!("Cancel result: {:?}", result);
            }
        }
    }

    Ok(())
}
