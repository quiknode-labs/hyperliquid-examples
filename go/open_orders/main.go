// Open Orders Example
//
// View all open orders with details.
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
	// Private key required to query your open orders
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

	// Get all open orders (pass empty string to use wallet address)
	result, err := sdk.OpenOrders("")
	if err != nil {
		log.Fatalf("Failed to get open orders: %v", err)
	}
	orderList, _ := result["orders"].([]any)
	fmt.Printf("Open orders: %d\n", len(orderList))

	for _, o := range orderList {
		order := o.(map[string]any)
		side := "BUY"
		if order["side"] == "A" {
			side = "SELL"
		}
		fmt.Printf("  %s %s %s @ %s (OID: %v)\n",
			order["coin"], side, order["sz"], order["limitPx"], order["oid"])
	}

	// Get order status for a specific order
	// status, _ := sdk.OrderStatus(12345, "")
	// fmt.Printf("Order status: %v\n", status)
}
