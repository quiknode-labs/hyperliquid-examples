//! Markets Example
//!
//! List all available markets and HIP-3 DEXes.
//!
//! No endpoint or private key needed — uses public API.
//!
//! # Usage
//! ```bash
//! cargo run --example markets
//! ```

use hyperliquid_sdk::HyperliquidSDK;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();

    // No endpoint or private key needed for read-only public queries
    let sdk = HyperliquidSDK::new().build().await?;

    // Get all markets
    let markets = sdk.markets().await?;

    if let Some(perps) = markets.get("perps").and_then(|v| v.as_array()) {
        println!("Perp markets: {}", perps.len());

        // Show first 5 perp markets
        println!("\nFirst 5 perp markets:");
        for m in perps.iter().take(5) {
            let name = m.get("name").and_then(|v| v.as_str()).unwrap_or("?");
            let sz_decimals = m.get("szDecimals").and_then(|v| v.as_u64()).unwrap_or(0);
            println!("  {}: szDecimals={}", name, sz_decimals);
        }
    }

    if let Some(spot) = markets.get("spot").and_then(|v| v.as_array()) {
        println!("\nSpot markets: {}", spot.len());
    }

    // Get HIP-3 DEXes
    let dexes = sdk.dexes().await?;
    if let Some(arr) = dexes.as_array() {
        println!("\nHIP-3 DEXes: {}", arr.len());
        for dex in arr.iter().take(5) {
            let name = dex.get("name").and_then(|v| v.as_str()).unwrap_or("N/A");
            println!("  {}", name);
        }
    }

    Ok(())
}
