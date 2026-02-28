//! Withdraw Example
//!
//! Withdraw USDC to L1 (Arbitrum).
//!
//! # Usage
//! ```bash
//! export PRIVATE_KEY=0x...
//! cargo run --example withdraw
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

    // Withdraw USDC to L1 (Arbitrum)
    // WARNING: This is a real withdrawal - be careful with amounts
    // let result = sdk.withdraw(
    //     "0x1234567890123456789012345678901234567890",  // Arbitrum address
    //     100.0
    // ).await?;
    // println!("Withdraw: {:?}", result);

    println!("Withdraw methods available:");
    println!("  sdk.withdraw(destination, amount)");
    println!("  Note: Withdraws USDC to your L1 Arbitrum address");

    Ok(())
}
