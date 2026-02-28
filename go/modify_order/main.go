// Modify Order Example
//
// Place a resting order and then modify its price.
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

	// Place a resting order
	mid, err := sdk.GetMid("BTC")
	if err != nil {
		log.Fatalf("Failed to get mid: %v", err)
	}
	limitPrice := math.Floor(mid * 0.97)
	order, err := sdk.Buy("BTC", hyperliquid.WithNotional(11), hyperliquid.WithPrice(limitPrice), hyperliquid.WithTIF(hyperliquid.TIFGTC))
	if err != nil {
		log.Fatalf("Failed to place order: %v", err)
	}
	fmt.Printf("Placed order at $%.0f\n", limitPrice)
	fmt.Printf("  OID: %d\n", order.OID)

	// Modify to a new price (4% below mid)
	newPrice := math.Floor(mid * 0.96)
	newPriceStr := fmt.Sprintf("%.0f", newPrice)
	newOrder, err := order.Modify(newPriceStr, order.Size)
	if err != nil {
		log.Fatalf("Failed to modify order: %v", err)
	}
	fmt.Printf("Modified to $%s\n", newPriceStr)
	fmt.Printf("  New OID: %d\n", newOrder.OID)

	// Clean up
	_, _ = newOrder.Cancel()
	fmt.Println("Order cancelled.")
}
