#!/usr/bin/env npx ts-node
/**
 * Builder Fee Example
 *
 * Approve and revoke builder fee permissions.
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

  // Check approval status (doesn't require deposit)
  const status = await sdk.approvalStatus();
  console.log(`Approval status: ${JSON.stringify(status)}`);

  // Approve builder fee (required before trading via QuickNode)
  // Note: Requires account to have deposited first
  // const result = await sdk.approveBuilderFee("1%");
  // console.log(`Approve builder fee: ${JSON.stringify(result)}`);

  // Revoke builder fee permission
  // const result = await sdk.revokeBuilderFee();
  // console.log(`Revoke builder fee: ${JSON.stringify(result)}`);

  console.log("\nBuilder fee methods available:");
  console.log("  sdk.approveBuilderFee(maxFee, builder?)");
  console.log("  sdk.revokeBuilderFee(builder?)");
  console.log("  sdk.approvalStatus(user?)");
}

main().catch(console.error);
