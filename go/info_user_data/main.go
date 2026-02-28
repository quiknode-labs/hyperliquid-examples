// User Account Data Example
//
// Shows how to query user positions, orders, and account state.
//
// Setup:
//     go build
//
// Usage:
//     export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
//     export USER_ADDRESS="0x..."
//     ./info_user_data
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
	user := os.Getenv("USER_ADDRESS")
	if user == "" {
		user = "0x2ba553d9f990a3b66b03b2dc0d030dfc1c061036"
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
	fmt.Printf("User Data: %s...\n", user[:10])
	fmt.Println("==================================================")

	// Clearinghouse state (positions + margin)
	fmt.Println("\n1. Positions & Margin:")
	state, err := info.ClearinghouseState(user)
	if err != nil {
		fmt.Printf("   (clearinghouse_state not available: %v)\n", err)
	} else {
		margin, _ := state["marginSummary"].(map[string]any)
		fmt.Printf("   Account Value: $%s\n", margin["accountValue"])
		fmt.Printf("   Margin Used: $%s\n", margin["totalMarginUsed"])

		positions, _ := state["assetPositions"].([]any)
		if len(positions) > 0 {
			fmt.Printf("   Positions: %d\n", len(positions))
			for i, pos := range positions {
				if i >= 3 {
					break
				}
				p := pos.(map[string]any)
				position := p["position"].(map[string]any)
				fmt.Printf("   - %s: %s @ %s\n", position["coin"], position["szi"], position["entryPx"])
			}
		} else {
			fmt.Println("   No positions")
		}
	}

	// Open orders
	fmt.Println("\n2. Open Orders:")
	orders, err := info.OpenOrders(user)
	if err != nil {
		fmt.Printf("   (open_orders not available: %v)\n", err)
	} else if len(orders) > 0 {
		fmt.Printf("   %d orders:\n", len(orders))
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
	} else {
		fmt.Println("   No open orders")
	}

	// User fees
	fmt.Println("\n3. Fee Structure:")
	fees, err := info.UserFees(user)
	if err != nil {
		fmt.Printf("   (user_fees not available: %v)\n", err)
	} else {
		fmt.Printf("   Maker: %v\n", fees["makerRate"])
		fmt.Printf("   Taker: %v\n", fees["takerRate"])
	}

	// Spot balances
	fmt.Println("\n4. Spot Balances:")
	spot, err := info.SpotClearinghouseState(user)
	if err != nil {
		fmt.Printf("   (spot_clearinghouse_state not available: %v)\n", err)
	} else {
		balances, _ := spot["balances"].([]any)
		if len(balances) > 0 {
			for i, b := range balances {
				if i >= 5 {
					break
				}
				bal := b.(map[string]any)
				fmt.Printf("   - %s: %s\n", bal["coin"], bal["total"])
			}
		} else {
			fmt.Println("   No spot balances")
		}
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
