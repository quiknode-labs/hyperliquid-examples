// Builder Fee Example
//
// Approve and revoke builder fee permissions.
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

	// Check approval status (doesn't require deposit)
	status, err := sdk.ApprovalStatus("")
	if err != nil {
		log.Printf("Failed to get approval status: %v", err)
	} else {
		fmt.Printf("Approval status: %v\n", status)
	}

	// Approve builder fee (required before trading via QuickNode)
	// Note: Requires account to have deposited first
	// result, err := sdk.ApproveBuilderFee("1%", "")
	// fmt.Printf("Approve builder fee: %v\n", result)

	// Revoke builder fee permission
	// result, err := sdk.RevokeBuilderFee("")
	// fmt.Printf("Revoke builder fee: %v\n", result)

	fmt.Println("\nBuilder fee methods available:")
	fmt.Println("  sdk.ApproveBuilderFee(maxFee, builder)")
	fmt.Println("  sdk.RevokeBuilderFee(builder)")
	fmt.Println("  sdk.ApprovalStatus(user)")
}
