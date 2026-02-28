#!/usr/bin/env npx ts-node
/**
 * Builder Fee Approval Example
 *
 * Approve the builder fee to enable trading through the API.
 * Required before placing orders.
 */

import { HyperliquidSDK } from 'hyperliquid-sdk';

async function main() {
  const sdk = new HyperliquidSDK();

  // Check current approval status
  const status = await sdk.approvalStatus();
  console.log(`Currently approved: ${status.approved ?? false}`);
  if (status.approved) {
    console.log(`Max fee rate: ${status.maxFeeRate}`);
  }

  // Approve builder fee (1% max)
  // await sdk.approveBuilderFee("1%");
  // console.log("Approved!");

  // Or use autoApprove when creating SDK:
  // const sdk = new HyperliquidSDK(endpoint, { autoApprove: true });

  // Revoke approval:
  // await sdk.revokeBuilderFee();
}

main().catch(console.error);
