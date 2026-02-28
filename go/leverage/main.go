// Leverage Example
//
// Update leverage for a position.
//
// Requires: PRIVATE_KEY environment variable
package main

import (
	"encoding/json"
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

	fmt.Printf("Wallet: %s\n", sdk.Address())

	// Update leverage for BTC to 10x cross margin (default)
	result, err := sdk.UpdateLeverage("BTC", 10)
	if err != nil {
		log.Printf("Failed to update leverage: %v", err)
	} else {
		jsonResult, _ := json.Marshal(result)
		fmt.Printf("Update leverage result: %s\n", jsonResult)
	}

	// Update leverage for ETH to 5x isolated margin
	// result, err := sdk.UpdateLeverage("ETH", 5, hyperliquid.LeverageWithIsolated())
	// fmt.Printf("Update leverage result: %v\n", result)

	fmt.Println("\nLeverage methods available:")
	fmt.Println("  sdk.UpdateLeverage(asset, leverage)  // cross margin")
	fmt.Println("  sdk.UpdateLeverage(asset, leverage, hyperliquid.LeverageWithIsolated())  // isolated")
}
