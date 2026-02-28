#!/usr/bin/env npx ts-node
/**
 * Staking Example
 *
 * Stake and unstake HYPE tokens.
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

  // Stake HYPE tokens
  // const result = await sdk.stake(100);
  // console.log(`Stake: ${JSON.stringify(result)}`);

  // Unstake HYPE tokens
  // const result = await sdk.unstake(50);
  // console.log(`Unstake: ${JSON.stringify(result)}`);

  // Delegate to a validator
  // const result = await sdk.delegate("0x...", 100);  // Validator address
  // console.log(`Delegate: ${JSON.stringify(result)}`);

  // Undelegate from a validator
  // const result = await sdk.undelegate("0x...", 50);  // Validator address
  // console.log(`Undelegate: ${JSON.stringify(result)}`);

  console.log("Staking methods available:");
  console.log("  sdk.stake(amount)");
  console.log("  sdk.unstake(amount)");
  console.log("  sdk.delegate(validator, amount)");
  console.log("  sdk.undelegate(validator, amount)");
}

main().catch(console.error);
