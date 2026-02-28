// Close Position Example
//
// Close an open position completely. The SDK figures out the size and direction.
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

	// Close BTC position (if any)
	// The SDK queries your position and builds the counter-order automatically
	result, err := sdk.ClosePosition("BTC")
	if err != nil {
		fmt.Printf("No position to close or error: %v\n", err)
	} else {
		fmt.Printf("Closed position: %v\n", result)
	}
}
