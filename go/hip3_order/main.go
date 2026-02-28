// HIP-3 Market Order Example
//
// Trade on HIP-3 markets (community perps like Hypersea).
// Same API as regular markets, just use "dex:symbol" format.
package main

import (
	"fmt"
	"log"
	"os"

	"github.com/quiknode-labs/raptor/hyperliquid-sdk/go/hyperliquid"
)

func main() {
	endpoint := os.Getenv("ENDPOINT")
	if endpoint == "" {
		endpoint = os.Getenv("QUICKNODE_ENDPOINT")
	}

	sdk, err := hyperliquid.New(endpoint)
	if err != nil {
		log.Fatalf("Failed to create SDK: %v", err)
	}

	// List HIP-3 DEXes
	dexes, err := sdk.Dexes()
	if err != nil {
		log.Fatalf("Failed to get dexes: %v", err)
	}

	fmt.Println("Available HIP-3 DEXes:")
	count := 0
	for _, dex := range dexes {
		if count >= 5 {
			break
		}
		if d, ok := dex.(map[string]any); ok {
			name, _ := d["name"].(string)
			fmt.Printf("  %s\n", name)
		} else if name, ok := dex.(string); ok {
			fmt.Printf("  %s\n", name)
		}
		count++
	}

	// Trade on a HIP-3 market
	// Format: "dex:SYMBOL"
	// order, _ := sdk.Buy("xyz:SILVER", hyperliquid.WithNotional(11), hyperliquid.WithTIF("ioc"))
	// fmt.Printf("HIP-3 order: %v\n", order)

	fmt.Println("\nHIP-3 markets use 'dex:SYMBOL' format")
	fmt.Println("Example: sdk.Buy(\"xyz:SILVER\", hyperliquid.WithNotional(11))")
}
