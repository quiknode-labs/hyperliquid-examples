//! Multi-User Queries Example
//!
//! Shows how to query multiple users' states efficiently.
//!
//! # Usage
//! ```bash
//! export ENDPOINT=https://your-endpoint.hype-mainnet.quiknode.pro/TOKEN
//! cargo run --example info_batch_queries
//! ```

use hyperliquid_sdk::HyperliquidSDK;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();

    let endpoint = std::env::var("ENDPOINT").expect("Set ENDPOINT environment variable");

    let sdk = HyperliquidSDK::new()
        .endpoint(&endpoint)
        .build()
        .await?;

    println!("==================================================");
    println!("Multi-User Queries");
    println!("==================================================");

    // Example addresses (use real addresses with activity for better demo)
    let addresses = [
        "0x2ba553d9f990a3b66b03b2dc0d030dfc1c061036",  // Active trader
        "0x0000000000000000000000000000000000000001",
        "0x0000000000000000000000000000000000000002",
    ];

    println!("\nQuerying {} user accounts...", addresses.len());

    // Query each user's clearinghouse state
    println!("\n1. User Account States:");
    for addr in &addresses {
        match sdk.info().clearinghouse_state(addr).await {
            Ok(state) => {
                let value = state
                    .get("marginSummary")
                    .and_then(|m| m.get("accountValue"))
                    .and_then(|v| v.as_str())
                    .and_then(|s| s.parse::<f64>().ok())
                    .unwrap_or(0.0);
                let positions = state
                    .get("assetPositions")
                    .and_then(|v| v.as_array())
                    .map(|a| a.len())
                    .unwrap_or(0);
                println!("   {}...: ${:.2} ({} positions)", &addr[..12], value, positions);
            }
            Err(e) => {
                println!("   {}...: Error - {}", &addr[..12], e);
            }
        }
    }

    // Query open orders for first user
    println!("\n2. Open Orders (first user):");
    match sdk.info().open_orders(addresses[0]).await {
        Ok(orders) => {
            if let Some(arr) = orders.as_array() {
                println!("   {} open orders", arr.len());
                for o in arr.iter().take(3) {
                    let coin = o.get("coin").and_then(|v| v.as_str()).unwrap_or("?");
                    let side = if o.get("side").and_then(|v| v.as_str()) == Some("B") { "BUY" } else { "SELL" };
                    let sz = o.get("sz").and_then(|v| v.as_str()).unwrap_or("?");
                    let px = o.get("limitPx").and_then(|v| v.as_str()).unwrap_or("?");
                    println!("   - {}: {} {} @ {}", coin, side, sz, px);
                }
            }
        }
        Err(e) => println!("   Error: {}", e),
    }

    // Query user fees
    println!("\n3. Fee Structure (first user):");
    match sdk.info().user_fees(addresses[0]).await {
        Ok(fees) => {
            let maker = fees.get("makerRate").and_then(|v| v.as_str()).unwrap_or("N/A");
            let taker = fees.get("takerRate").and_then(|v| v.as_str()).unwrap_or("N/A");
            println!("   Maker: {}", maker);
            println!("   Taker: {}", taker);
        }
        Err(e) => println!("   Error: {}", e),
    }

    println!("\n==================================================");
    println!("Done!");

    Ok(())
}
