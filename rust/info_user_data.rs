//! User Account Data Example
//!
//! Shows how to query user positions, orders, and account state.
//!
//! # Usage
//! ```bash
//! export ENDPOINT=https://your-endpoint.hype-mainnet.quiknode.pro/TOKEN
//! export USER_ADDRESS=0x...
//! cargo run --example info_user_data
//! ```

use hyperliquid_sdk::HyperliquidSDK;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();

    let endpoint = std::env::var("ENDPOINT").expect("Set ENDPOINT environment variable");
    let user = std::env::var("USER_ADDRESS")
        .unwrap_or_else(|_| "0x2ba553d9f990a3b66b03b2dc0d030dfc1c061036".to_string());

    let sdk = HyperliquidSDK::new()
        .endpoint(&endpoint)
        .build()
        .await?;

    println!("==================================================");
    println!("User Data: {}...", &user[..10]);
    println!("==================================================");

    // Clearinghouse state (positions + margin)
    println!("\n1. Positions & Margin:");
    match sdk.info().clearinghouse_state(&user).await {
        Ok(state) => {
            if let Some(margin) = state.get("marginSummary") {
                let value = margin.get("accountValue").and_then(|v| v.as_str()).unwrap_or("0");
                let used = margin.get("totalMarginUsed").and_then(|v| v.as_str()).unwrap_or("0");
                println!("   Account Value: ${}", value);
                println!("   Margin Used: ${}", used);
            }

            if let Some(positions) = state.get("assetPositions").and_then(|v| v.as_array()) {
                if positions.is_empty() {
                    println!("   No positions");
                } else {
                    println!("   Positions: {}", positions.len());
                    for pos in positions.iter().take(3) {
                        if let Some(p) = pos.get("position") {
                            let coin = p.get("coin").and_then(|v| v.as_str()).unwrap_or("?");
                            let szi = p.get("szi").and_then(|v| v.as_str()).unwrap_or("?");
                            let entry = p.get("entryPx").and_then(|v| v.as_str()).unwrap_or("?");
                            println!("   - {}: {} @ {}", coin, szi, entry);
                        }
                    }
                }
            }
        }
        Err(e) => println!("   (clearinghouse_state not available: {})", e),
    }

    // Open orders
    println!("\n2. Open Orders:");
    match sdk.info().open_orders(&user).await {
        Ok(orders) => {
            if let Some(arr) = orders.as_array() {
                if arr.is_empty() {
                    println!("   No open orders");
                } else {
                    println!("   {} orders:", arr.len());
                    for o in arr.iter().take(3) {
                        let coin = o.get("coin").and_then(|v| v.as_str()).unwrap_or("?");
                        let side = if o.get("side").and_then(|v| v.as_str()) == Some("B") { "BUY" } else { "SELL" };
                        let sz = o.get("sz").and_then(|v| v.as_str()).unwrap_or("?");
                        let px = o.get("limitPx").and_then(|v| v.as_str()).unwrap_or("?");
                        println!("   - {}: {} {} @ {}", coin, side, sz, px);
                    }
                }
            }
        }
        Err(e) => println!("   (open_orders not available: {})", e),
    }

    // User fees
    println!("\n3. Fee Structure:");
    match sdk.info().user_fees(&user).await {
        Ok(fees) => {
            let maker = fees.get("makerRate").and_then(|v| v.as_str()).unwrap_or("N/A");
            let taker = fees.get("takerRate").and_then(|v| v.as_str()).unwrap_or("N/A");
            println!("   Maker: {}", maker);
            println!("   Taker: {}", taker);
        }
        Err(e) => println!("   (user_fees not available: {})", e),
    }

    // Spot balances
    println!("\n4. Spot Balances:");
    match sdk.info().spot_clearinghouse_state(&user).await {
        Ok(spot) => {
            if let Some(balances) = spot.get("balances").and_then(|v| v.as_array()) {
                if balances.is_empty() {
                    println!("   No spot balances");
                } else {
                    for b in balances.iter().take(5) {
                        let coin = b.get("coin").and_then(|v| v.as_str()).unwrap_or("?");
                        let total = b.get("total").and_then(|v| v.as_str()).unwrap_or("?");
                        println!("   - {}: {}", coin, total);
                    }
                }
            }
        }
        Err(e) => println!("   (spot_clearinghouse_state not available: {})", e),
    }

    println!("\n==================================================");
    println!("Done!");

    Ok(())
}
