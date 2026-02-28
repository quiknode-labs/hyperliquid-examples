// Isolated Margin Example
//
// Add or remove margin from an isolated position.
//
// Requires: PRIVATE_KEY environment variable
package main

import (
	"fmt"
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

	sdk, _ := hyperliquid.New("", hyperliquid.WithPrivateKey(privateKey))
	fmt.Printf("Wallet: %s\n", sdk.Address())

	// Add $100 margin to BTC long position (isBuy=true for long)
	// result, err := sdk.UpdateIsolatedMargin("BTC", 100, true)
	// fmt.Printf("Add margin result: %v\n", result)

	// Remove $50 margin from ETH short position (isBuy=false for short)
	// result, err := sdk.UpdateIsolatedMargin("ETH", -50, false)
	// fmt.Printf("Remove margin result: %v\n", result)

	// Top up isolated-only margin (special maintenance mode)
	// result, err := sdk.TopUpIsolatedOnlyMargin("BTC", 100)
	// fmt.Printf("Top up isolated-only margin result: %v\n", result)

	fmt.Println("\nIsolated margin methods available:")
	fmt.Println("  sdk.UpdateIsolatedMargin(asset, amount, isBuy)")
	fmt.Println("  sdk.TopUpIsolatedOnlyMargin(asset, amount)")
}
