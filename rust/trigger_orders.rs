//! Trigger Orders Example
//!
//! Stop loss and take profit orders.
//!
//! # Usage
//! ```bash
//! export PRIVATE_KEY=0x...
//! cargo run --example trigger_orders
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

    let mid = sdk.get_mid("BTC").await?;
    println!("BTC mid: ${:.2}", mid);

    // Stop loss order (market) - triggers when price falls below stop price
    // No limit_price means market order when triggered
    // let result = sdk.stop_loss(
    //     "BTC",
    //     0.001,
    //     mid * 0.95,  // 5% below current
    //     None,        // Market order when triggered
    //     Side::Sell,
    // ).await?;
    // println!("Stop loss (market): {:?}", result);

    // Stop loss order (limit) - triggers and places limit order at limit_price
    // let result = sdk.stop_loss(
    //     "BTC",
    //     0.001,
    //     mid * 0.95,
    //     Some(mid * 0.94),
    //     Side::Sell,
    // ).await?;
    // println!("Stop loss (limit): {:?}", result);

    // Take profit order (market) - triggers when price rises above trigger
    // let result = sdk.take_profit(
    //     "BTC",
    //     0.001,
    //     mid * 1.05,  // 5% above current
    //     None,        // Market order when triggered
    //     Side::Sell,
    // ).await?;
    // println!("Take profit (market): {:?}", result);

    // Take profit order (limit)
    // let result = sdk.take_profit(
    //     "BTC",
    //     0.001,
    //     mid * 1.05,
    //     Some(mid * 1.06),
    //     Side::Sell,
    // ).await?;
    // println!("Take profit (limit): {:?}", result);

    // For buy-side stop/TP (e.g., closing a short position), use Side::Buy
    // let result = sdk.stop_loss("BTC", 0.001, mid * 1.05, None, Side::Buy).await?;

    println!("\nTrigger order methods available:");
    println!("  sdk.stop_loss(asset, size, trigger_price, limit_price, side)");
    println!("  sdk.take_profit(asset, size, trigger_price, limit_price, side)");
    println!("  sdk.trigger_order(TriggerOrder {{ ... }})");
    println!("\nNote: Omit limit_price (None) for market orders when triggered");

    Ok(())
}
