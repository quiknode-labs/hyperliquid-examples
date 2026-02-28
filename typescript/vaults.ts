#!/usr/bin/env npx ts-node
/**
 * Vaults Example
 *
 * Deposit and withdraw from Hyperliquid vaults.
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

  // Example vault address (HLP vault)
  const HLP_VAULT = "0xdfc24b077bc1425ad1dea75bcb6f8158e10df303";

  // Deposit to vault
  // const result = await sdk.vaultDeposit(HLP_VAULT, 100.0);
  // console.log(`Vault deposit: ${JSON.stringify(result)}`);

  // Withdraw from vault
  // const result = await sdk.vaultWithdraw(HLP_VAULT, 50.0);
  // console.log(`Vault withdraw: ${JSON.stringify(result)}`);

  console.log("Vault methods available:");
  console.log("  sdk.vaultDeposit(vaultAddress, amount)");
  console.log("  sdk.vaultWithdraw(vaultAddress, amount)");
}

main().catch(console.error);
