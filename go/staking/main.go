// Staking Example
//
// Stake and unstake HYPE tokens.
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

	_, _ = hyperliquid.New("", hyperliquid.WithPrivateKey(privateKey))

	// Stake HYPE tokens
	// result, _ := sdk.Stake(100)
	// fmt.Printf("Stake: %v\n", result)

	// Unstake HYPE tokens
	// result, _ := sdk.Unstake(50)
	// fmt.Printf("Unstake: %v\n", result)

	// Delegate to a validator
	// result, _ := sdk.Delegate("0x...", 100)  // Validator address, amount
	// fmt.Printf("Delegate: %v\n", result)

	// Undelegate from a validator
	// result, _ := sdk.Undelegate("0x...", 50)  // Validator address, amount
	// fmt.Printf("Undelegate: %v\n", result)

	fmt.Println("Staking methods available:")
	fmt.Println("  sdk.Stake(amount)")
	fmt.Println("  sdk.Unstake(amount)")
	fmt.Println("  sdk.Delegate(validator, amount)")
	fmt.Println("  sdk.Undelegate(validator, amount)")
}
