//! HyperEVM Example
//!
//! Shows how to use standard Ethereum JSON-RPC calls on Hyperliquid's EVM chain.
//!
//! # Usage
//! ```bash
//! export ENDPOINT=https://your-endpoint.hype-mainnet.quiknode.pro/TOKEN
//! cargo run --example evm_basics
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
    println!("HyperEVM (Ethereum JSON-RPC)");
    println!("==================================================");

    // Chain info
    println!("\n1. Chain Info:");
    let chain_id = sdk.evm().chain_id().await?;
    let block_num = sdk.evm().block_number().await?;
    let gas_price = sdk.evm().gas_price().await?;
    println!("   Chain ID: {}", chain_id);
    println!("   Block: {}", block_num);
    println!("   Gas Price: {:.2} gwei", gas_price as f64 / 1e9);

    // Latest block
    println!("\n2. Latest Block:");
    if let Some(block) = sdk.evm().get_block_by_number("latest").await? {
        if let Some(hash) = block.get("hash").and_then(|v| v.as_str()) {
            println!("   Hash: {}...", &hash[..20.min(hash.len())]);
        }
        if let Some(txs) = block.get("transactions").and_then(|v| v.as_array()) {
            println!("   Txs: {}", txs.len());
        }
    }

    // Check balance
    println!("\n3. Balance Check:");
    let addr = "0x0000000000000000000000000000000000000000";
    let balance = sdk.evm().get_balance(addr).await?;
    println!("   {}...: {:.6} ETH", &addr[..12], balance as f64 / 1e18);

    println!("\n==================================================");
    println!("Done!");
    println!("\nFor debug/trace APIs, use EVM with debug=true");

    Ok(())
}
