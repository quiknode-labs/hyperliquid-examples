//! Modify Order Example
//!
//! Place a resting order and then modify its price.
//!
//! # Usage
//! ```bash
//! export PRIVATE_KEY=0x...
//! cargo run --example modify_order
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

    // Place a resting order
    let mid = sdk.get_mid("BTC").await?;
    let limit_price = (mid * 0.97) as i64;

    let order = sdk.limit_buy("BTC", limit_price as f64, 0.0001).await?;
    println!("Placed order at ${}", limit_price);
    println!("  OID: {:?}", order.oid);

    // Modify to a new price (4% below mid)
    let new_price = (mid * 0.96) as i64;
    if let Some(oid) = order.oid {
        let new_order = sdk.modify_order(oid, "BTC", Some(new_price as f64), None).await?;
        println!("Modified to ${}", new_price);
        println!("  New OID: {:?}", new_order.oid);

        // Clean up
        if let Some(new_oid) = new_order.oid {
            sdk.cancel(new_oid, "BTC").await?;
            println!("Order cancelled.");
        }
    }

    Ok(())
}
