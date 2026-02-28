//! Fluent Builder Example
//!
//! Demonstrates the fluent/chainable API for building orders.
//! This is the recommended approach for power users.
//!
//! # Usage
//! ```bash
//! export PRIVATE_KEY=0x...
//! export ENDPOINT=https://your-endpoint.hype-mainnet.quiknode.pro/TOKEN
//! cargo run --example fluent_builder
//! ```

use hyperliquid_sdk::{HyperliquidSDK, Order, TriggerOrder};

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
    // Fluent Order Builder
    // ─────────────────────────────────────────────────────────────────────────

    // Build and place a limit buy order
    println!("\n1. Building limit buy order with fluent API...");
    let order = Order::buy("BTC")
        .size(0.001)
        .price(50000.0)
        .gtc();

    println!("Order built:");
    println!("  Asset: {}", order.get_asset());
    println!("  Side: {:?}", order.get_side());
    println!("  Size: {:?}", order.get_size());
    println!("  Price: {:?}", order.get_price());
    println!("  TIF: {:?}", order.get_tif());

    // Place the order
    let placed = sdk.order(order).await?;
    println!("Order placed: {:?}", placed.oid);

    if placed.is_resting() {
        let _ = placed.cancel().await;
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Market Order with Notional
    // ─────────────────────────────────────────────────────────────────────────

    println!("\n2. Building market order by notional...");
    let order = Order::sell("ETH")
        .notional(100.0)
        .market();

    println!("Order built:");
    println!("  Asset: {}", order.get_asset());
    println!("  Side: {:?}", order.get_side());
    println!("  Notional: {:?}", order.get_notional());
    println!("  Is market: {}", order.is_market());

    // let placed = sdk.order(order).await?;
    // println!("Order placed: {:?}", placed.oid);

    // ─────────────────────────────────────────────────────────────────────────
    // Post-Only Order
    // ─────────────────────────────────────────────────────────────────────────

    println!("\n3. Building post-only (ALO) order...");
    let order = Order::long("BTC")  // 'long' is alias for 'buy'
        .size(0.001)
        .price(45000.0)
        .alo()  // Add-Liquidity-Only / Post-Only
        .random_cloid();  // Generate random client order ID

    println!("Order built:");
    println!("  Has CLOID: {}", order.get_cloid().is_some());

    // ─────────────────────────────────────────────────────────────────────────
    // Reduce-Only Order
    // ─────────────────────────────────────────────────────────────────────────

    println!("\n4. Building reduce-only order...");
    let order = Order::short("BTC")  // 'short' is alias for 'sell'
        .size(0.001)
        .price(70000.0)
        .gtc()
        .reduce_only();

    println!("Order built:");
    println!("  Reduce only: {}", order.is_reduce_only());

    // ─────────────────────────────────────────────────────────────────────────
    // Trigger Orders (Stop-Loss / Take-Profit)
    // ─────────────────────────────────────────────────────────────────────────

    println!("\n5. Building stop-loss trigger order...");
    let trigger = TriggerOrder::stop_loss("BTC")
        .size(0.001)
        .trigger_price(40000.0)
        .market();  // Execute as market when triggered

    println!("Trigger order built:");
    println!("  Type: {:?}", trigger.get_tpsl());
    println!("  Trigger price: {:?}", trigger.get_trigger_price());
    println!("  Is market: {}", trigger.is_market());

    // let placed = sdk.trigger_order(trigger).await?;
    // println!("Trigger order placed: {:?}", placed.oid);

    println!("\n6. Building take-profit trigger order with limit...");
    let trigger = TriggerOrder::take_profit("ETH")
        .size(1.0)
        .trigger_price(5000.0)
        .limit(4990.0);  // Execute as limit when triggered

    println!("Trigger order built:");
    println!("  Type: {:?}", trigger.get_tpsl());
    println!("  Trigger price: {:?}", trigger.get_trigger_price());
    println!("  Limit price: {:?}", trigger.get_limit_price());
    println!("  Is market: {}", trigger.is_market());

    // ─────────────────────────────────────────────────────────────────────────
    // Order Validation
    // ─────────────────────────────────────────────────────────────────────────

    println!("\n7. Validating order before submission...");
    let order = Order::buy("BTC")
        .size(0.001)
        .price(50000.0)
        .gtc();

    match order.validate() {
        Ok(()) => println!("  ✓ Order is valid"),
        Err(e) => println!("  ✗ Validation failed: {}", e),
    }

    // Invalid order (no size or notional)
    let invalid_order = Order::buy("BTC")
        .price(50000.0)
        .gtc();

    match invalid_order.validate() {
        Ok(()) => println!("  ✓ Order is valid"),
        Err(e) => println!("  ✗ Validation failed: {}", e),
    }

    Ok(())
}
