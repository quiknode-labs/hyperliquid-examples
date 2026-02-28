// Cancel All Orders Example
//
// Cancel all open orders, or all orders for a specific asset.
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

	// Check open orders first (pass empty string to use wallet address)
	orders, err := sdk.OpenOrders("")
	if err != nil {
		log.Printf("Failed to get open orders: %v", err)
	} else {
		orderList, _ := orders["orders"].([]any)
		fmt.Printf("Open orders: %d\n", len(orderList))
	}

	// Cancel all orders
	result, err := sdk.CancelAll("")
	if err != nil {
		fmt.Printf("Cancel all: {\"message\": \"No orders to cancel\"}\n")
	} else {
		fmt.Printf("Cancel all: %v\n", result)
	}

	// Or cancel just BTC orders:
	// sdk.CancelAll("BTC")
}
