//! Builder Fee Example
//!
//! Approve and revoke builder fee permissions.
//!
//! # Usage
//! ```bash
//! export PRIVATE_KEY=0x...
//! cargo run --example builder_fee
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

    // Check approval status (doesn't require deposit)
    let status = sdk.approval_status().await?;
    println!("Approval status: {:?}", status);

    // Approve builder fee (required before trading via QuickNode)
    // Note: Requires account to have deposited first
    // let result = sdk.approve_builder_fee(Some("1%")).await?;
    // println!("Approve builder fee: {:?}", result);

    // Revoke builder fee permission
    // let result = sdk.revoke_builder_fee().await?;
    // println!("Revoke builder fee: {:?}", result);

    println!("\nBuilder fee methods available:");
    println!("  sdk.approve_builder_fee(max_fee)");
    println!("  sdk.revoke_builder_fee()");
    println!("  sdk.approval_status()");

    Ok(())
}
