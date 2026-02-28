//! Transfers Example
//!
//! Transfer USD and spot assets between accounts and wallets.
//!
//! # Usage
//! ```bash
//! export PRIVATE_KEY=0x...
//! cargo run --example transfers
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

    // Transfer USD to another address
    // let result = sdk.transfer_usd(
    //     "0x1234567890123456789012345678901234567890",
    //     10.0
    // ).await?;
    // println!("USD transfer: {:?}", result);

    // Transfer spot asset to another address
    // let result = sdk.transfer_spot(
    //     "PURR",  // or token index
    //     "0x1234567890123456789012345678901234567890",
    //     100.0
    // ).await?;
    // println!("Spot transfer: {:?}", result);

    // Transfer from spot wallet to perp wallet (internal)
    // let result = sdk.transfer_spot_to_perp(100.0).await?;
    // println!("Spot to perp: {:?}", result);

    // Transfer from perp wallet to spot wallet (internal)
    // let result = sdk.transfer_perp_to_spot(100.0).await?;
    // println!("Perp to spot: {:?}", result);

    // Send asset (generalized transfer)
    // let result = sdk.send_asset(
    //     "USDC",  // or token index
    //     "100.0",
    //     "0x1234567890123456789012345678901234567890"
    // ).await?;
    // println!("Send asset: {:?}", result);

    println!("Transfer methods available:");
    println!("  sdk.transfer_usd(destination, amount)");
    println!("  sdk.transfer_spot(token, destination, amount)");
    println!("  sdk.transfer_spot_to_perp(amount)");
    println!("  sdk.transfer_perp_to_spot(amount)");
    println!("  sdk.send_asset(token, amount, destination)");

    Ok(())
}
