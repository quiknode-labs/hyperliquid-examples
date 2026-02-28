// Preflight Validation Example
//
// Validate an order BEFORE signing to catch tick size and lot size errors.
// Saves failed transactions by checking validity upfront.
//
// No endpoint or private key needed — uses public API.
package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math"
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

	// Get current price
	mid, err := sdk.GetMid("BTC")
	if err != nil {
		log.Fatalf("Failed to get mid: %v", err)
	}
	fmt.Printf("BTC mid: $%.2f\n", mid)

	// Validate a good order
	result, err := sdk.Preflight("BTC", "buy", math.Floor(mid*0.97), 0.001)
	if err != nil {
		log.Printf("Preflight error: %v", err)
	} else {
		jsonResult, _ := json.Marshal(result)
		fmt.Printf("Valid order: %s\n", jsonResult)
	}

	// Validate an order with too many decimals (will fail)
	result, err = sdk.Preflight("BTC", "buy", 67000.123456789, 0.001)
	if err != nil {
		log.Printf("Preflight error: %v", err)
	} else {
		jsonResult, _ := json.Marshal(result)
		fmt.Printf("Invalid price: %s\n", jsonResult)
		if valid, ok := result["valid"].(bool); ok && !valid {
			fmt.Printf("  Error: %v\n", result["error"])
			fmt.Printf("  Suggestion: %v\n", result["suggestion"])
		}
	}
}
