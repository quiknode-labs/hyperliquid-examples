//! Preflight Validation Example
//!
//! Validate an order BEFORE signing to catch tick size and lot size errors.
//! Saves failed transactions by checking validity upfront.
//!
//! No endpoint or private key needed — uses public API.
//!
//! # Usage
//! ```bash
//! cargo run --example preflight
//! ```

use hyperliquid_sdk::HyperliquidSDK;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();

    // No endpoint or private key needed for read-only public queries
    let sdk = HyperliquidSDK::new().build().await?;

    // Get current price
    let mid = sdk.get_mid("BTC").await?;
    println!("BTC mid: ${:.2}", mid);

    // Validate a good order
    let limit_price = (mid * 0.97) as i64;
    let result = sdk.preflight("BTC", "buy", Some(limit_price as f64), Some(0.001)).await?;
    println!("Valid order: {:?}", result);

    // Validate an order with too many decimals (will fail)
    let result = sdk.preflight("BTC", "buy", Some(67000.123456789), Some(0.001)).await?;
    println!("Invalid price: {:?}", result);

    let valid = result.get("valid").and_then(|v| v.as_bool()).unwrap_or(true);
    if !valid {
        if let Some(error) = result.get("error").and_then(|v| v.as_str()) {
            println!("  Error: {}", error);
        }
        if let Some(suggestion) = result.get("suggestion").and_then(|v| v.as_str()) {
            println!("  Suggestion: {}", suggestion);
        }
    }

    Ok(())
}
