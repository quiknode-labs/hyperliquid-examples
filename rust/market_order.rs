//! Market Order Example
//!
//! Demonstrates placing market buy and sell orders.
//!
//! # Usage
//! ```bash
//! export PRIVATE_KEY=0x...
//! export ENDPOINT=https://your-endpoint.hype-mainnet.quiknode.pro/TOKEN
//! cargo run --example market_order
//! ```

use hyperliquid_sdk::HyperliquidSDK;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize tracing for better debugging
    tracing_subscriber::fmt::init();

    // Build the SDK
    // - If PRIVATE_KEY env var is set, it will be used automatically
    // - If ENDPOINT env var is set, use it; otherwise uses public worker
    let endpoint = std::env::var("ENDPOINT").ok();

    let mut builder = HyperliquidSDK::new();
    if let Some(ep) = endpoint {
        builder = builder.endpoint(ep);
    }

    let sdk = builder.build().await?;

    println!("SDK initialized for address: {:?}", sdk.address());

    // ─────────────────────────────────────────────────────────────────────────
    // Market Buy
    // ─────────────────────────────────────────────────────────────────────────

    // Option 1: Buy by notional value ($11 worth of BTC)
    println!("\nPlacing market buy order for $11 worth of BTC...");
    let order = sdk.market_buy("BTC").await.notional(11.0).await?;

    println!("Order result:");
    println!("  Status: {}", order.status);
    println!("  OID: {:?}", order.oid);
    println!("  Filled size: {:?}", order.filled_size);
    println!("  Average price: {:?}", order.avg_price);

    // Option 2: Buy by size (0.0001 BTC)
    println!("\nPlacing market buy order for 0.0001 BTC...");
    let order = sdk.market_buy("BTC").await.size(0.0001).await?;

    println!("Order result:");
    println!("  Status: {}", order.status);
    println!("  OID: {:?}", order.oid);

    // ─────────────────────────────────────────────────────────────────────────
    // Market Sell
    // ─────────────────────────────────────────────────────────────────────────

    // Market sell by notional
    println!("\nPlacing market sell order for $11 worth of ETH...");
    let order = sdk.market_sell("ETH").await.notional(11.0).await?;

    println!("Order result:");
    println!("  Status: {}", order.status);
    println!("  OID: {:?}", order.oid);

    // ─────────────────────────────────────────────────────────────────────────
    // Error Handling
    // ─────────────────────────────────────────────────────────────────────────

    if order.is_error() {
        println!("\nOrder failed: {:?}", order.error);
        println!("Guidance: Check your margin and position size.");
    }

    Ok(())
}
