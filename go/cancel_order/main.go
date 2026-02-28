// Cancel Order Example
//
// Place an order and then cancel it by OID.
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

	// Place a resting order 3% below mid
	mid, err := sdk.GetMid("BTC")
	if err != nil {
		log.Fatalf("Failed to get mid: %v", err)
	}
	limitPrice := math.Floor(mid * 0.97)

	order, err := sdk.Buy("BTC", hyperliquid.WithNotional(11), hyperliquid.WithPrice(limitPrice), hyperliquid.WithTIF(hyperliquid.TIFGTC))
	if err != nil {
		log.Fatalf("Failed to place order: %v", err)
	}
	fmt.Printf("Placed order OID: %d\n", order.OID)

	// Cancel using the order object
	_, err = order.Cancel()
	if err != nil {
		log.Printf("Failed to cancel: %v", err)
	} else {
		fmt.Println("Cancelled via order.Cancel()")
	}

	// Alternative: cancel by OID directly
	// sdk.Cancel(12345, "BTC")
}
