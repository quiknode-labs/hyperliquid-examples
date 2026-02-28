//! Historical Candles Example
//!
//! Shows how to fetch historical candlestick (OHLCV) data.
//!
//! Note: candleSnapshot may not be available on all QuickNode endpoints.
//! Check the QuickNode docs for method availability.
//!
//! # Usage
//! ```bash
//! export ENDPOINT=https://your-endpoint.hype-mainnet.quiknode.pro/TOKEN
//! cargo run --example info_candles
//! ```

use hyperliquid_sdk::HyperliquidSDK;
use std::time::{SystemTime, UNIX_EPOCH};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();

    let endpoint = std::env::var("ENDPOINT").expect("Set ENDPOINT environment variable");

    let sdk = HyperliquidSDK::new()
        .endpoint(&endpoint)
        .build()
        .await?;

    println!("==================================================");
    println!("Historical Candles");
    println!("==================================================");

    // Last 24 hours
    let now = SystemTime::now()
        .duration_since(UNIX_EPOCH)?
        .as_millis() as u64;
    let day_ago = now - (24 * 60 * 60 * 1000);

    // Fetch BTC 1-hour candles
    println!("\n1. BTC 1-Hour Candles (last 24h):");
    match sdk.info().candles("BTC", "1h", day_ago, now).await {
        Ok(candles) => {
            if let Some(arr) = candles.as_array() {
                println!("   Retrieved {} candles", arr.len());
                for c in arr.iter().rev().take(3) {
                    let o = c.get("o").and_then(|v| v.as_str()).unwrap_or("?");
                    let h = c.get("h").and_then(|v| v.as_str()).unwrap_or("?");
                    let l = c.get("l").and_then(|v| v.as_str()).unwrap_or("?");
                    let close = c.get("c").and_then(|v| v.as_str()).unwrap_or("?");
                    println!("   O:{} H:{} L:{} C:{}", o, h, l, close);
                }
            }
        }
        Err(e) => {
            println!("   Error: {}", e);
            println!("   Note: candleSnapshot may not be available on this endpoint");
        }
    }

    // Predicted funding rates (supported on QuickNode)
    println!("\n2. Predicted Funding Rates:");
    match sdk.info().predicted_fundings().await {
        Ok(fundings) => {
            if let Some(arr) = fundings.as_array() {
                println!("   {} assets with funding rates:", arr.len());
                let mut count = 0;
                for item in arr {
                    if count >= 5 {
                        break;
                    }
                    if let Some(inner) = item.as_array() {
                        if inner.len() >= 2 {
                            let coin = inner[0].as_str().unwrap_or("?");
                            if let Some(sources) = inner[1].as_array() {
                                for src in sources {
                                    if let Some(src_arr) = src.as_array() {
                                        if src_arr.len() >= 2 && src_arr[0].as_str() == Some("HlPerp") {
                                            if let Some(rate) = src_arr[1]
                                                .get("fundingRate")
                                                .and_then(|v| v.as_str())
                                                .and_then(|s| s.parse::<f64>().ok())
                                            {
                                                println!("   {}: {:.4}%", coin, rate * 100.0);
                                                count += 1;
                                                break;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        Err(e) => println!("   Error: {}", e),
    }

    println!("\n==================================================");
    println!("Done!");

    Ok(())
}
