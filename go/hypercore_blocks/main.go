// HyperCore Block Data Example
//
// Shows how to get real-time trades, orders, and block data via the HyperCore API.
//
// This is the alternative to Info methods (allMids, l2Book, recentTrades) that
// are not available on QuickNode endpoints.
//
// Setup:
//     go build
//
// Usage:
//     export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
//     ./hypercore_blocks
package main

import (
	"fmt"
	"log"
	"os"

	"github.com/quiknode-labs/raptor/hyperliquid-sdk/go/hyperliquid"
)

func main() {
	endpoint := os.Getenv("ENDPOINT")
	if endpoint == "" {
		endpoint = os.Getenv("QUICKNODE_ENDPOINT")
	}
	if endpoint == "" {
		fmt.Println("Set ENDPOINT environment variable")
		os.Exit(1)
	}

	sdk, err := hyperliquid.New(endpoint)
	if err != nil {
		log.Fatalf("Failed to create SDK: %v", err)
	}
	hc := sdk.Core()

	fmt.Println("==================================================")
	fmt.Println("HyperCore Block Data")
	fmt.Println("==================================================")

	// Latest block number
	fmt.Println("\n1. Latest Block:")
	blockNum, err := hc.LatestBlockNumber()
	if err != nil {
		log.Fatalf("Failed to get block number: %v", err)
	}
	fmt.Printf("   Block #%d\n", blockNum)

	// Recent trades (returns []map[string]any)
	fmt.Println("\n2. Recent Trades (all coins):")
	trades, err := hc.LatestTrades(5, "")
	if err != nil {
		log.Printf("Failed to get trades: %v", err)
	} else {
		for i, trade := range trades {
			if i >= 5 {
				break
			}
			side := "BUY"
			if trade["side"] == "A" {
				side = "SELL"
			}
			fmt.Printf("   %s %s %s @ $%s\n", side, trade["sz"], trade["coin"], trade["px"])
		}
	}

	// Recent BTC trades only
	fmt.Println("\n3. BTC Trades:")
	btcTrades, err := hc.LatestTrades(10, "BTC")
	if err != nil {
		log.Printf("Failed to get BTC trades: %v", err)
	} else if len(btcTrades) > 0 {
		for i, trade := range btcTrades {
			if i >= 3 {
				break
			}
			side := "BUY"
			if trade["side"] == "A" {
				side = "SELL"
			}
			fmt.Printf("   %s %s @ $%s\n", side, trade["sz"], trade["px"])
		}
	} else {
		fmt.Println("   No BTC trades in recent blocks")
	}

	// Get a specific block
	fmt.Println("\n4. Get Block Data:")
	block, err := hc.GetBlock(blockNum - 1)
	if err != nil {
		log.Printf("Failed to get block: %v", err)
	} else {
		fmt.Printf("   Block #%d\n", blockNum-1)
		fmt.Printf("   Time: %v\n", block["block_time"])
		events, _ := block["events"].([]any)
		fmt.Printf("   Events: %d\n", len(events))
	}

	// Get batch of blocks (returns []any)
	fmt.Println("\n5. Batch Blocks:")
	batchBlocks, err := hc.GetBatchBlocks(blockNum-5, blockNum-1)
	if err != nil {
		log.Printf("Failed to get batch blocks: %v", err)
	} else {
		fmt.Printf("   Retrieved %d blocks\n", len(batchBlocks))
	}

	fmt.Println("\n==================================================")
	fmt.Println("Done!")
}
