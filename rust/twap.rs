//! TWAP Orders Example
//!
//! Time-Weighted Average Price orders for large trades.
//!
//! # Usage
//! ```bash
//! export PRIVATE_KEY=0x...
//! cargo run --example twap
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

    // TWAP order - executes over time to minimize market impact
    // let result = sdk.twap_order(
    //     "BTC",
    //     0.01,           // Total size to execute
    //     true,           // is_buy
    //     60,             // duration_minutes: Execute over 60 minutes
    //     true,           // randomize: Randomize execution times
    //     false,          // reduce_only
    // ).await?;
    // println!("TWAP order: {:?}", result);
    //
    // // Extract twap_id from response
    // let twap_id = result
    //     .get("response")
    //     .and_then(|r| r.get("data"))
    //     .and_then(|d| d.get("running"))
    //     .and_then(|r| r.get("id"))
    //     .and_then(|i| i.as_u64())
    //     .unwrap_or(0);

    // Cancel TWAP order
    // let result = sdk.twap_cancel("BTC", twap_id).await?;
    // println!("TWAP cancel: {:?}", result);

    println!("\nTWAP methods available:");
    println!("  sdk.twap_order(asset, size, is_buy, duration_minutes, randomize, reduce_only)");
    println!("  sdk.twap_cancel(asset, twap_id)");

    Ok(())
}
