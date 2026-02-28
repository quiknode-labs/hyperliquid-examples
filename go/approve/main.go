// Builder Fee Approval Example
//
// Approve the builder fee to enable trading through the API.
// Required before placing orders.
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

	// Check current approval status
	status, err := sdk.ApprovalStatus("")
	if err != nil {
		log.Printf("Failed to get approval status: %v", err)
	} else {
		approved, _ := status["approved"].(bool)
		fmt.Printf("Currently approved: %v\n", approved)
		if approved {
			maxFeeRate, _ := status["maxFeeRate"].(string)
			fmt.Printf("Max fee rate: %s\n", maxFeeRate)
		}
	}

	// Approve builder fee (1% max)
	// result, err := sdk.ApproveBuilderFee("1%", "")
	// fmt.Printf("Approved: %v\n", result)

	// Or use WithAutoApprove when creating SDK:
	// sdk, _ := hyperliquid.New(endpoint, hyperliquid.WithAutoApprove(true))

	// Revoke approval:
	// sdk.RevokeBuilderFee("")
}
