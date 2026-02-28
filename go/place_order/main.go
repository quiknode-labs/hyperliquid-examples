// Limit Order Example
//
// Place a limit order that rests on the book until filled or cancelled.
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

	// Get current price
	mid, err := sdk.GetMid("BTC")
	if err != nil {
		log.Fatalf("Failed to get mid: %v", err)
	}
	fmt.Printf("BTC mid price: $%.2f\n", mid)

	// Place limit buy 3% below mid (GTC = Good Till Cancelled)
	limitPrice := math.Floor(mid * 0.97)
	order, err := sdk.Buy("BTC", hyperliquid.WithNotional(11), hyperliquid.WithPrice(limitPrice), hyperliquid.WithTIF("gtc"))
	if err != nil {
		log.Fatalf("Failed to place order: %v", err)
	}

	fmt.Println("Placed limit order:")
	fmt.Printf("  OID: %d\n", order.OID)
	fmt.Printf("  Price: $%.0f\n", limitPrice)
	fmt.Printf("  Status: %s\n", order.Status)

	// Clean up - cancel the order
	order.Cancel()
	fmt.Println("Order cancelled.")
}
