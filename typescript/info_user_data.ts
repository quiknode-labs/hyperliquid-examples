#!/usr/bin/env npx ts-node
/**
 * User Account Data Example
 *
 * Shows how to query user positions, orders, and account state.
 *
 * Setup:
 *     npm install hyperliquid-sdk
 *
 * Usage:
 *     export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
 *     export USER_ADDRESS="0x..."
 *     npx ts-node info_user_data.ts
 */

import { HyperliquidSDK, HyperliquidError } from 'hyperliquid-sdk';

const ENDPOINT = process.env.ENDPOINT;
const USER = process.env.USER_ADDRESS || "0x2ba553d9f990a3b66b03b2dc0d030dfc1c061036";

if (!ENDPOINT) {
  console.log("Set ENDPOINT environment variable");
  process.exit(1);
}

async function main() {
  // Single SDK instance — access everything through sdk.info, sdk.core, sdk.evm, etc.
  const sdk = new HyperliquidSDK(ENDPOINT);
  const info = sdk.info;

  console.log("=".repeat(50));
  console.log(`User Data: ${USER.slice(0, 10)}...`);
  console.log("=".repeat(50));

  // Clearinghouse state (positions + margin)
  console.log("\n1. Positions & Margin:");
  try {
    const state = await info.clearinghouseState(USER) as Record<string, unknown>;
    const margin = (state.marginSummary || {}) as Record<string, unknown>;
    console.log(`   Account Value: $${margin.accountValue || '0'}`);
    console.log(`   Margin Used: $${margin.totalMarginUsed || '0'}`);

    const positions = (state.assetPositions || []) as unknown[];
    if (positions.length) {
      console.log(`   Positions: ${positions.length}`);
      for (const pos of positions.slice(0, 3)) {
        const p = ((pos as Record<string, unknown>).position || {}) as Record<string, unknown>;
        console.log(`   - ${p.coin}: ${p.szi} @ ${p.entryPx}`);
      }
    } else {
      console.log("   No positions");
    }
  } catch (e) {
    if (e instanceof HyperliquidError) {
      console.log(`   (clearinghouseState not available: ${e.code})`);
    }
  }

  // Open orders
  console.log("\n2. Open Orders:");
  try {
    const orders = await info.openOrders(USER) as unknown[];
    if (orders.length) {
      console.log(`   ${orders.length} orders:`);
      for (const o of orders.slice(0, 3)) {
        const order = o as Record<string, unknown>;
        const side = order.side === "B" ? "BUY" : "SELL";
        console.log(`   - ${order.coin}: ${side} ${order.sz} @ ${order.limitPx}`);
      }
    } else {
      console.log("   No open orders");
    }
  } catch (e) {
    if (e instanceof HyperliquidError) {
      console.log(`   (openOrders not available: ${e.code})`);
    }
  }

  // User fees
  console.log("\n3. Fee Structure:");
  try {
    const fees = await info.userFees(USER) as Record<string, unknown>;
    console.log(`   Maker: ${fees.makerRate || 'N/A'}`);
    console.log(`   Taker: ${fees.takerRate || 'N/A'}`);
  } catch (e) {
    if (e instanceof HyperliquidError) {
      console.log(`   (userFees not available: ${e.code})`);
    }
  }

  // Spot balances
  console.log("\n4. Spot Balances:");
  try {
    const spot = await info.spotClearinghouseState(USER) as Record<string, unknown>;
    const balances = (spot.balances || []) as unknown[];
    if (balances.length) {
      for (const b of balances.slice(0, 5)) {
        const balance = b as Record<string, unknown>;
        console.log(`   - ${balance.coin}: ${balance.total}`);
      }
    } else {
      console.log("   No spot balances");
    }
  } catch (e) {
    if (e instanceof HyperliquidError) {
      console.log(`   (spotClearinghouseState not available: ${e.code})`);
    }
  }

  console.log("\n" + "=".repeat(50));
  console.log("Done!");
}

main().catch(console.error);
