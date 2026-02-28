//! Full SDK Demo
//!
//! Demonstrates all SDK capabilities in one file.
//!
//! # Usage
//! ```bash
//! export PRIVATE_KEY=0x...
//! export ENDPOINT=https://your-endpoint.hype-mainnet.quiknode.pro/TOKEN
//! cargo run --example full_demo
//! ```

use hyperliquid_sdk::HyperliquidSDK;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();

    // ============================================================================
    // INITIALIZATION
    // ============================================================================

    let endpoint = std::env::var("ENDPOINT").ok();

    let mut builder = HyperliquidSDK::new();
    if let Some(ep) = endpoint {
        builder = builder.endpoint(ep);
    }

    // Alternative: with auto-approval
    // builder = builder.auto_approve(true);

    let sdk = builder.build().await?;

    println!("Wallet: {:?}\n", sdk.address());

    // ============================================================================
    // MARKET DATA
    // ============================================================================

    println!("=== Market Data ===");

    let mid = sdk.get_mid("BTC").await?;
    println!("BTC mid: ${:.2}", mid);

    let markets = sdk.markets().await?;
    if let Some(perps) = markets.get("perps").and_then(|v| v.as_array()) {
        println!("Perp markets: {}", perps.len());
    }
    if let Some(spot) = markets.get("spot").and_then(|v| v.as_array()) {
        println!("Spot markets: {}", spot.len());
    }

    let dexes = sdk.dexes().await?;
    if let Some(arr) = dexes.as_array() {
        println!("HIP-3 DEXes: {}", arr.len());
    }

    // ============================================================================
    // APPROVAL STATUS
    // ============================================================================

    println!("\n=== Approval Status ===");

    let status = sdk.approval_status().await?;
    let approved = status.get("approved").and_then(|v| v.as_bool()).unwrap_or(false);
    println!("Approved: {}", approved);
    if approved {
        if let Some(max_fee) = status.get("maxFeeRate").and_then(|v| v.as_str()) {
            println!("Max fee: {}", max_fee);
        }
    }

    // ============================================================================
    // ORDER VALIDATION (PREFLIGHT)
    // ============================================================================

    println!("\n=== Preflight Validation ===");

    let limit_price = (mid * 0.97) as i64;
    let result = sdk.preflight("BTC", "buy", Some(limit_price as f64), Some(0.001)).await?;
    let valid = result.get("valid").and_then(|v| v.as_bool()).unwrap_or(true);
    println!("Valid order: {}", valid);

    // ============================================================================
    // OPEN ORDERS
    // ============================================================================

    println!("\n=== Open Orders ===");

    let orders = sdk.open_orders().await?;
    if let Some(arr) = orders.as_array() {
        println!("Open orders: {}", arr.len());
        for o in arr.iter().take(3) {
            let name = o.get("coin").and_then(|v| v.as_str()).unwrap_or("?");
            let side = if o.get("side").and_then(|v| v.as_str()) == Some("B") { "BUY" } else { "SELL" };
            let sz = o.get("sz").and_then(|v| v.as_str()).unwrap_or("?");
            let px = o.get("limitPx").and_then(|v| v.as_str()).unwrap_or("?");
            let oid = o.get("oid").and_then(|v| v.as_u64()).unwrap_or(0);
            println!("  {} {} {} @ {} (OID: {})", name, side, sz, px, oid);
        }
    }

    // ============================================================================
    // ORDER PLACEMENT (commented to avoid real trades)
    // ============================================================================

    println!("\n=== Order Methods ===");
    println!("Available order methods:");
    println!("  sdk.market_buy(asset).await.notional(usd).await?");
    println!("  sdk.market_buy(asset).await.size(qty).await?");
    println!("  sdk.market_sell(asset).await.notional(usd).await?");
    println!("  sdk.limit_buy(asset, price, size).await?");
    println!("  sdk.limit_sell(asset, price, size).await?");
    println!("  sdk.order(Order::buy(...).size(...).price(...).gtc())");

    // ============================================================================
    // ORDER MANAGEMENT (commented to avoid real actions)
    // ============================================================================

    println!("\n=== Order Management ===");
    println!("Available management methods:");
    println!("  order.cancel().await?               // Cancel via order object");
    println!("  order.modify(price, size).await?    // Modify via order object");
    println!("  sdk.cancel(oid, asset).await?       // Cancel by OID");
    println!("  sdk.cancel_by_cloid(cloid, asset)?  // Cancel by client order ID");
    println!("  sdk.cancel_all(None).await?         // Cancel all orders");
    println!("  sdk.cancel_all(Some(\"BTC\")).await?  // Cancel all BTC orders");
    println!("  sdk.close_position(\"BTC\").await?    // Close a position");

    // ============================================================================
    // FLUENT ORDER BUILDER
    // ============================================================================

    println!("\n=== Fluent Order Builder ===");
    println!("Order::buy(\"BTC\")");
    println!("  .size(0.001)       // Size in asset units");
    println!("  .notional(100)     // Size in USD");
    println!("  .price(65000)      // Limit price");
    println!("  .gtc()             // Good Till Cancelled");
    println!("  .ioc()             // Immediate Or Cancel");
    println!("  .alo()             // Add Liquidity Only");
    println!("  .market()          // Market order");
    println!("  .reduce_only()     // Only close position");

    println!("\n=== Demo Complete ===");

    Ok(())
}
