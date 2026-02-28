//! Open Orders Example
//!
//! View all open orders with details.
//!
//! # Usage
//! ```bash
//! export PRIVATE_KEY=0x...
//! cargo run --example open_orders
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

    // Get all open orders
    let orders = sdk.open_orders().await?;

    if let Some(arr) = orders.as_array() {
        println!("Open orders: {}", arr.len());

        for o in arr {
            let name = o.get("coin").and_then(|v| v.as_str()).unwrap_or("?");
            let side = if o.get("side").and_then(|v| v.as_str()) == Some("B") { "BUY" } else { "SELL" };
            let sz = o.get("sz").and_then(|v| v.as_str()).unwrap_or("?");
            let px = o.get("limitPx").and_then(|v| v.as_str()).unwrap_or("?");
            let oid = o.get("oid").and_then(|v| v.as_u64()).unwrap_or(0);
            println!("  {} {} {} @ {} (OID: {})", name, side, sz, px, oid);
        }
    }

    // Get order status for a specific order
    // let status = sdk.order_status(12345).await?;
    // println!("Order status: {:?}", status);

    Ok(())
}
