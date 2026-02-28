#!/usr/bin/env npx ts-node
/**
 * Transfers Example
 *
 * Transfer USD and spot assets between accounts and wallets.
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

  // Transfer USD to another address
  // const result = await sdk.transferUsd(
  //   "0x1234567890123456789012345678901234567890",
  //   10.0
  // );
  // console.log(`USD transfer: ${JSON.stringify(result)}`);

  // Transfer spot asset to another address
  // const result = await sdk.transferSpot(
  //   "PURR",  // token (or token index)
  //   "0x1234567890123456789012345678901234567890",  // destination
  //   100.0    // amount
  // );
  // console.log(`Spot transfer: ${JSON.stringify(result)}`);

  // Transfer from spot wallet to perp wallet (internal)
  // const result = await sdk.transferSpotToPerp(100.0);
  // console.log(`Spot to perp: ${JSON.stringify(result)}`);

  // Transfer from perp wallet to spot wallet (internal)
  // const result = await sdk.transferPerpToSpot(100.0);
  // console.log(`Perp to spot: ${JSON.stringify(result)}`);

  // Send asset (generalized transfer)
  // const result = await sdk.sendAsset(
  //   "USDC",  // token (or token index)
  //   100.0,   // amount
  //   "0x1234567890123456789012345678901234567890"  // destination
  // );
  // console.log(`Send asset: ${JSON.stringify(result)}`);

  console.log("Transfer methods available:");
  console.log("  sdk.transferUsd(destination, amount)");
  console.log("  sdk.transferSpot(token, destination, amount)");
  console.log("  sdk.transferSpotToPerp(amount)");
  console.log("  sdk.transferPerpToSpot(amount)");
  console.log("  sdk.sendAsset(token, amount, destination)");
}

main().catch(console.error);
