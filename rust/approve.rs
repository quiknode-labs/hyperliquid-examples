//! Builder Fee Approval Example
//!
//! Approve the builder fee to enable trading through the API.
//! Required before placing orders.
//!
//! # Usage
//! ```bash
//! export PRIVATE_KEY=0x...
//! cargo run --example approve
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

    // Check current approval status
    let status = sdk.approval_status().await?;
    println!("Approval status: {:?}", status);

    if let Some(approved) = status.get("approved").and_then(|v| v.as_bool()) {
        println!("Currently approved: {}", approved);
        if approved {
            if let Some(max_fee) = status.get("maxFeeRate").and_then(|v| v.as_str()) {
                println!("Max fee rate: {}", max_fee);
            }
        }
    }

    // Approve builder fee (1% max)
    // Uncomment to approve:
    // let result = sdk.approve_builder_fee(Some("1%")).await?;
    // println!("Approval result: {:?}", result);

    // Or use auto_approve when creating SDK:
    // let sdk = HyperliquidSDK::new()
    //     .auto_approve(true)
    //     .build()
    //     .await?;

    Ok(())
}
