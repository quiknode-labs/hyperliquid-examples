//! Schedule Cancel Example (Dead Man's Switch)
//!
//! Schedule automatic cancellation of all orders after a delay.
//! If you don't send another schedule_cancel before the time expires,
//! all your orders are cancelled. Useful as a safety mechanism.
//!
//! NOTE: Requires $1M trading volume on your account to use this feature.
//!
//! # Usage
//! ```bash
//! export PRIVATE_KEY=0x...
//! cargo run --example schedule_cancel
//! ```

use hyperliquid_sdk::HyperliquidSDK;
use std::time::{SystemTime, UNIX_EPOCH};

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

    // Schedule cancel all orders in 60 seconds
    let now = SystemTime::now()
        .duration_since(UNIX_EPOCH)?
        .as_millis() as u64;
    let cancel_time = now + 60000; // 60 seconds from now

    // let result = sdk.schedule_cancel(Some(cancel_time)).await?;
    // println!("Scheduled cancel at {}: {:?}", cancel_time, result);

    // To cancel the scheduled cancel (keep orders alive):
    // let result = sdk.schedule_cancel(None).await?;
    // println!("Cancelled scheduled cancel: {:?}", result);

    println!("Schedule cancel methods available:");
    println!("  sdk.schedule_cancel(Some(time_ms))  // Schedule cancel at timestamp");
    println!("  sdk.schedule_cancel(None)           // Cancel the scheduled cancel");
    println!("\nNOTE: Requires $1M trading volume on your account");
    println!("Example cancel time: {} (60 seconds from now)", cancel_time);

    Ok(())
}
