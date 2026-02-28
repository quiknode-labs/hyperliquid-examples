// TWAP Orders Example
//
// Time-Weighted Average Price orders for large trades.
//
// Requires: PRIVATE_KEY environment variable
package main

import (
	"fmt"
	"log"
	"os"

	"github.com/quiknode-labs/raptor/hyperliquid-sdk/go/hyperliquid"
)

func main() {
	privateKey := os.Getenv("PRIVATE_KEY")
	if privateKey == "" {
		fmt.Println("Set PRIVATE_KEY environment variable")
		fmt.Println("Example: export PRIVATE_KEY='0x...'")
		os.Exit(1)
	}

	sdk, err := hyperliquid.New("", hyperliquid.WithPrivateKey(privateKey))
	if err != nil {
		log.Fatalf("Failed to create SDK: %v", err)
	}

	mid, err := sdk.GetMid("BTC")
	if err != nil {
		log.Fatalf("Failed to get mid: %v", err)
	}
	fmt.Printf("BTC mid: $%.2f\n", mid)

	// TWAP order - executes over time to minimize market impact
	// result, _ := sdk.TwapOrder("BTC", 0.01, true, 60, true, false)
	//   - asset: "BTC"
	//   - size: 0.01 (total size to execute)
	//   - isBuy: true
	//   - durationMinutes: 60 (execute over 60 minutes)
	//   - randomize: true (randomize execution times)
	//   - reduceOnly: false
	// fmt.Printf("TWAP order: %v\n", result)
	// twapId := result["response"].(map[string]any)["data"].(map[string]any)["running"].(map[string]any)["id"]

	// Cancel TWAP order
	// result, _ := sdk.TwapCancel("BTC", twapId)
	// fmt.Printf("TWAP cancel: %v\n", result)

	fmt.Println("\nTWAP methods available:")
	fmt.Println("  sdk.TwapOrder(asset, size, isBuy, durationMinutes, randomize, reduceOnly)")
	fmt.Println("  sdk.TwapCancel(asset, twapId)")
}
