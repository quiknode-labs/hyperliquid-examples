#!/usr/bin/env npx ts-node
/**
 * Withdraw Example
 *
 * Withdraw USDC to L1 (Arbitrum).
 *
 * Requires: PRIVATE_KEY environment variable
 */

import { HyperliquidSDK } from 'hyperliquid-sdk';

async function main() {
  const privateKey = process.env.PRIVATE_KEY;
  if (!privateKey) {
    console.log("Set PRIVATE_KEY environment variable");
    console.log("Example: export PRIVATE_KEY='0x...'");
    process.exit(1);
  }

  const sdk = new HyperliquidSDK(undefined, { privateKey });
  console.log(`Wallet: ${sdk.address}`);

  // Withdraw USDC to L1 (Arbitrum)
  // WARNING: This is a real withdrawal - be careful with amounts
  // const result = await sdk.withdraw(
  //     "0x1234567890123456789012345678901234567890",  // Arbitrum address
  //     100.0
  // );
  // console.log(`Withdraw: ${JSON.stringify(result)}`);

  console.log("Withdraw methods available:");
  console.log("  sdk.withdraw(destination, amount)");
  console.log("  Note: Withdraws USDC to your L1 Arbitrum address");
}

main().catch(console.error);
