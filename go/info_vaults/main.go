// Vaults & Delegation Example
//
// Shows how to query vault information and user delegations.
//
// Setup:
//     go build
//
// Usage:
//     export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
//     export USER_ADDRESS="0x..."  # Optional
//     ./info_vaults
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
	user := os.Getenv("USER_ADDRESS")

	if endpoint == "" {
		fmt.Println("Set ENDPOINT environment variable")
		os.Exit(1)
	}

	sdk, err := hyperliquid.New(endpoint)
	if err != nil {
		log.Fatalf("Failed to create SDK: %v", err)
	}
	info := sdk.Info()

	fmt.Println("==================================================")
	fmt.Println("Vaults & Delegation")
	fmt.Println("==================================================")

	// Vault summaries
	fmt.Println("\n1. Vault Summaries:")
	vaults, err := info.VaultSummaries()
	if err != nil {
		fmt.Printf("   Error: %v\n", err)
	} else {
		fmt.Printf("   Total: %d\n", len(vaults))
		for i, v := range vaults {
			if i >= 3 {
				break
			}
			vault := v.(map[string]any)
			fmt.Printf("   - %s: TVL $%v\n", vault["name"], vault["tvl"])
		}
	}

	// User delegations
	if user != "" {
		fmt.Printf("\n2. Delegations (%s...):\n", user[:10])
		delegations, err := info.Delegations(user)
		if err != nil {
			fmt.Printf("   Error: %v\n", err)
		} else if len(delegations) > 0 {
			fmt.Printf("   %d active\n", len(delegations))
		} else {
			fmt.Println("   None")
		}
	} else {
		fmt.Println("\n(Set USER_ADDRESS for delegation info)")
	}

	fmt.Println("\n==================================================")
	fmt.Println("Done!")
}
