// Markets Example
//
// List all available markets and HIP-3 DEXes.
//
// No endpoint or private key needed — uses public API.
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

	// No endpoint or private key needed for read-only public queries
	sdk, err := hyperliquid.New(endpoint)
	if err != nil {
		log.Fatalf("Failed to create SDK: %v", err)
	}

	// Get all markets (returns *hyperliquid.Markets struct)
	markets, err := sdk.Markets()
	if err != nil {
		log.Fatalf("Failed to get markets: %v", err)
	}

	fmt.Printf("Perp markets: %d\n", len(markets.Perps))
	fmt.Printf("Spot markets: %d\n", len(markets.Spot))

	// Show first 5 perp markets
	fmt.Println("\nFirst 5 perp markets:")
	for i, m := range markets.Perps {
		if i >= 5 {
			break
		}
		fmt.Printf("  %s: szDecimals=%d\n", m.Name, m.SzDecimals)
	}

	// Get HIP-3 DEXes
	dexes, err := sdk.Dexes()
	if err != nil {
		log.Fatalf("Failed to get dexes: %v", err)
	}
	fmt.Printf("\nHIP-3 DEXes: %d\n", len(dexes))
	count := 0
	for name := range dexes {
		if count >= 5 {
			break
		}
		fmt.Printf("  %s\n", name)
		count++
	}
}
