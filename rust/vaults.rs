//! Vaults Example
//!
//! Deposit and withdraw from Hyperliquid vaults.
//!
//! # Usage
//! ```bash
//! export PRIVATE_KEY=0x...
//! cargo run --example vaults
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

    // Example vault address (HLP vault)
    let hlp_vault = "0xdfc24b077bc1425ad1dea75bcb6f8158e10df303";

    // Deposit to vault
    // let result = sdk.vault_deposit(hlp_vault, 100.0).await?;
    // println!("Vault deposit: {:?}", result);

    // Withdraw from vault
    // let result = sdk.vault_withdraw(hlp_vault, 50.0).await?;
    // println!("Vault withdraw: {:?}", result);

    println!("Vault methods available:");
    println!("  sdk.vault_deposit(vault_address, amount)");
    println!("  sdk.vault_withdraw(vault_address, amount)");
    println!("\nExample vault (HLP): {}", hlp_vault);

    Ok(())
}
