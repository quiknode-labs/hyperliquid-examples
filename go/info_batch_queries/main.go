// Multi-User Queries Example
//
// Shows how to query multiple users' states efficiently.
//
// Setup:
//     go build
//
// Usage:
//     export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
//     ./info_batch_queries
package main

import (
	"fmt"
	"log"
	"os"
	"strconv"

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
	info := sdk.Info()

	fmt.Println("==================================================")
	fmt.Println("Multi-User Queries")
	fmt.Println("==================================================")

	// Example addresses (use real addresses with activity for better demo)
	addresses := []string{
		"0x2ba553d9f990a3b66b03b2dc0d030dfc1c061036", // Active trader
		"0x0000000000000000000000000000000000000001",
		"0x0000000000000000000000000000000000000002",
	}

	fmt.Printf("\nQuerying %d user accounts...\n", len(addresses))

	// Query each user's clearinghouse state
	fmt.Println("\n1. User Account States:")
	for _, addr := range addresses {
		state, err := info.ClearinghouseState(addr)
		if err != nil {
			fmt.Printf("   %s...: Error - %v\n", addr[:12], err)
			continue
		}
		margin, _ := state["marginSummary"].(map[string]any)
		value := parseFloat(margin["accountValue"])
		positions, _ := state["assetPositions"].([]any)
		fmt.Printf("   %s...: $%.3f (%d positions)\n", addr[:12], value, len(positions))
	}

	// Query open orders for first user
	fmt.Println("\n2. Open Orders (first user):")
	orders, err := info.OpenOrders(addresses[0])
	if err != nil {
		fmt.Printf("   Error: %v\n", err)
	} else {
		fmt.Printf("   %d open orders\n", len(orders))
		for i, o := range orders {
			if i >= 3 {
				break
			}
			order := o.(map[string]any)
			side := "BUY"
			if order["side"] == "A" {
				side = "SELL"
			}
			fmt.Printf("   - %s: %s %s @ %s\n", order["coin"], side, order["sz"], order["limitPx"])
		}
	}

	// Query user fees
	fmt.Println("\n3. Fee Structure (first user):")
	fees, err := info.UserFees(addresses[0])
	if err != nil {
		fmt.Printf("   Error: %v\n", err)
	} else {
		fmt.Printf("   Maker: %v\n", fees["makerRate"])
		fmt.Printf("   Taker: %v\n", fees["takerRate"])
	}

	fmt.Println("\n==================================================")
	fmt.Println("Done!")
}

func parseFloat(v any) float64 {
	switch val := v.(type) {
	case string:
		f, _ := strconv.ParseFloat(val, 64)
		return f
	case float64:
		return val
	default:
		return 0
	}
}
