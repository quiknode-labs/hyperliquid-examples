//! Limit Order Example
//!
//! Demonstrates placing limit orders with different time-in-force options.
//!
//! # Usage
//! ```bash
//! export PRIVATE_KEY=0x...
//! export ENDPOINT=https://your-endpoint.hype-mainnet.quiknode.pro/TOKEN
//! cargo run --example place_order
//! ```

use hyperliquid_sdk::{HyperliquidSDK, TIF};

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

    // ─────────────────────────────────────────────────────────────────────────
    // GTC (Good-Till-Cancel) Order
    // ─────────────────────────────────────────────────────────────────────────

    // Place a limit buy order that stays on the book until filled or cancelled
    println!("\nPlacing GTC limit buy order...");
    let order = sdk.buy("BTC", 0.001, 50000.0, TIF::Gtc).await?;

    println!("GTC Order result:");
    println!("  Status: {}", order.status);
    println!("  OID: {:?}", order.oid);
    println!("  Price: {:?}", order.price);
    println!("  Size: {}", order.size);

    if order.is_resting() {
        println!("  ✓ Order is resting on the book");

        // Cancel the order
        println!("\nCancelling order...");
        let cancel_result = order.cancel().await?;
        println!("Cancel result: {:?}", cancel_result);
    }

    // ─────────────────────────────────────────────────────────────────────────
    // IOC (Immediate-or-Cancel) Order
    // ─────────────────────────────────────────────────────────────────────────

    // Place an IOC order - fills immediately or cancels
    println!("\nPlacing IOC limit buy order...");
    let order = sdk.buy("ETH", 0.1, 2000.0, TIF::Ioc).await?;

    println!("IOC Order result:");
    println!("  Status: {}", order.status);
    if order.is_filled() {
        println!("  ✓ Order filled immediately");
        println!("  Filled size: {:?}", order.filled_size);
        println!("  Avg price: {:?}", order.avg_price);
    }

    // ─────────────────────────────────────────────────────────────────────────
    // ALO (Add-Liquidity-Only / Post-Only) Order
    // ─────────────────────────────────────────────────────────────────────────

    // Place an ALO order - rejected if it would cross the spread
    println!("\nPlacing ALO (post-only) order...");
    let order = sdk.buy("BTC", 0.001, 40000.0, TIF::Alo).await?;

    println!("ALO Order result:");
    println!("  Status: {}", order.status);
    if order.is_resting() {
        println!("  ✓ Order added to book as maker");
        let _ = order.cancel().await;
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Sell Orders
    // ─────────────────────────────────────────────────────────────────────────

    println!("\nPlacing limit sell order...");
    let order = sdk.sell("BTC", 0.001, 100000.0, TIF::Gtc).await?;

    println!("Sell Order result:");
    println!("  Status: {}", order.status);
    println!("  Side: {}", order.side);

    if order.is_resting() {
        let _ = order.cancel().await;
    }

    Ok(())
}
