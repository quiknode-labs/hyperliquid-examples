// Withdraw Example
//
// Withdraw USDC to L1 (Arbitrum).
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

	// Withdraw USDC to L1 (Arbitrum)
	// WARNING: This is a real withdrawal - be careful with amounts
	// result, _ := sdk.Withdraw("0x1234567890123456789012345678901234567890", 100.0)
	// fmt.Printf("Withdraw: %v\n", result)

	fmt.Println("Withdraw methods available:")
	fmt.Println("  sdk.Withdraw(destination, amount)")
	fmt.Println("  Note: Withdraws USDC to your L1 Arbitrum address")
}
