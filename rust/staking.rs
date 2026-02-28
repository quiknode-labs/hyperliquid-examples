//! Staking Example
//!
//! Stake and unstake HYPE tokens.
//!
//! # Usage
//! ```bash
//! export PRIVATE_KEY=0x...
//! cargo run --example staking
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

    // Stake HYPE tokens
    // let result = sdk.stake(100.0).await?;
    // println!("Stake: {:?}", result);

    // Unstake HYPE tokens
    // let result = sdk.unstake(50.0).await?;
    // println!("Unstake: {:?}", result);

    // Delegate to a validator
    // let result = sdk.delegate("0x...", 100.0).await?;
    // println!("Delegate: {:?}", result);

    // Undelegate from a validator
    // let result = sdk.undelegate("0x...", 50.0).await?;
    // println!("Undelegate: {:?}", result);

    println!("Staking methods available:");
    println!("  sdk.stake(amount)");
    println!("  sdk.unstake(amount)");
    println!("  sdk.delegate(validator, amount)");
    println!("  sdk.undelegate(validator, amount)");

    Ok(())
}
