// Fluent Order Builder Example
//
// For power users who want maximum control with IDE autocomplete.
package main

import (
	"fmt"
	"log"
	"math"
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

	// Simple limit order with GTC (Good Till Cancelled) - minimum $10 value
	// Use size directly to ensure proper decimal precision (BTC allows 5 decimals)
	orderSpec := hyperliquid.Order().
		Buy("BTC").
		Size(0.00017). // ~$11 worth at ~$65k (minimum is $10)
		Price(math.Floor(mid * 0.97)).
		GTC()

	order, err := sdk.PlaceOrder(orderSpec)
	if err != nil {
		log.Fatalf("Failed to place order: %v", err)
	}
	fmt.Printf("Limit GTC: %v\n", order)

	order.Cancel()

	// Market order by notional value
	// orderSpec := hyperliquid.Order().
	//     Sell("ETH").
	//     Notional(10).
	//     Market()
	// order, _ := sdk.PlaceOrder(orderSpec)
	// fmt.Printf("Market: %v\n", order)

	// Reduce-only order (only closes existing position)
	// orderSpec := hyperliquid.Order().
	//     Sell("BTC").
	//     Size(0.001).
	//     Price(mid * 1.03).
	//     GTC().
	//     ReduceOnly()
	// order, _ := sdk.PlaceOrder(orderSpec)
	// fmt.Printf("Reduce-only: %v\n", order)

	// ALO order (Add Liquidity Only / Post-Only)
	// orderSpec := hyperliquid.Order().
	//     Buy("BTC").
	//     Size(0.001).
	//     Price(mid * 0.95).
	//     ALO()
	// order, _ := sdk.PlaceOrder(orderSpec)
	// fmt.Printf("Post-only: %v\n", order)

	fmt.Println("\nFluent builder methods:")
	fmt.Println("  .Size(0.001)       - Set size in asset units")
	fmt.Println("  .Notional(100)     - Set size in USD")
	fmt.Println("  .Price(65000)      - Set limit price")
	fmt.Println("  .GTC()             - Good Till Cancelled")
	fmt.Println("  .IOC()             - Immediate Or Cancel")
	fmt.Println("  .ALO()             - Add Liquidity Only (post-only)")
	fmt.Println("  .Market()          - Market order")
	fmt.Println("  .ReduceOnly()      - Only close position")
}
