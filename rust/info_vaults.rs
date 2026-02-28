//! Vaults & Delegation Example
//!
//! Shows how to query vault information and user delegations.
//!
//! # Usage
//! ```bash
//! export ENDPOINT=https://your-endpoint.hype-mainnet.quiknode.pro/TOKEN
//! export USER_ADDRESS=0x...  # Optional
//! cargo run --example info_vaults
//! ```

use hyperliquid_sdk::HyperliquidSDK;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();

    let endpoint = std::env::var("ENDPOINT").expect("Set ENDPOINT environment variable");
    let user = std::env::var("USER_ADDRESS").ok();

    let sdk = HyperliquidSDK::new()
        .endpoint(&endpoint)
        .build()
        .await?;

    println!("==================================================");
    println!("Vaults & Delegation");
    println!("==================================================");

    // Vault summaries
    println!("\n1. Vault Summaries:");
    match sdk.info().vault_summaries().await {
        Ok(vaults) => {
            if let Some(arr) = vaults.as_array() {
                println!("   Total: {}", arr.len());
                for v in arr.iter().take(3) {
                    let name = v.get("name").and_then(|v| v.as_str()).unwrap_or("N/A");
                    let tvl = v.get("tvl").and_then(|v| v.as_str()).unwrap_or("?");
                    println!("   - {}: TVL ${}", name, tvl);
                }
            }
        }
        Err(e) => println!("   Error: {}", e),
    }

    // User delegations
    if let Some(addr) = &user {
        println!("\n2. Delegations ({}...):", &addr[..10]);
        match sdk.info().delegations(addr).await {
            Ok(delegations) => {
                if let Some(arr) = delegations.as_array() {
                    if arr.is_empty() {
                        println!("   None");
                    } else {
                        println!("   {} active", arr.len());
                    }
                }
            }
            Err(e) => println!("   Error: {}", e),
        }
    } else {
        println!("\n(Set USER_ADDRESS for delegation info)");
    }

    println!("\n==================================================");
    println!("Done!");

    Ok(())
}
