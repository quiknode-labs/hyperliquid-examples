// Transfers Example
//
// Transfer USD and spot assets between accounts and wallets.
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

	// Transfer USD to another address
	// result, _ := sdk.TransferUsd("0x1234567890123456789012345678901234567890", 10.0)
	// fmt.Printf("USD transfer: %v\n", result)

	// Transfer spot asset to another address
	// result, _ := sdk.TransferSpot("PURR", "0x1234567890123456789012345678901234567890", 100.0)
	// fmt.Printf("Spot transfer: %v\n", result)

	// Transfer from spot wallet to perp wallet (internal)
	// result, _ := sdk.TransferSpotToPerp(100.0)
	// fmt.Printf("Spot to perp: %v\n", result)

	// Transfer from perp wallet to spot wallet (internal)
	// result, _ := sdk.TransferPerpToSpot(100.0)
	// fmt.Printf("Perp to spot: %v\n", result)

	// Send asset (generalized transfer)
	// result, _ := sdk.SendAsset("USDC", 100.0, "0x1234567890123456789012345678901234567890", nil)
	// fmt.Printf("Send asset: %v\n", result)

	fmt.Println("Transfer methods available:")
	fmt.Println("  sdk.TransferUsd(destination, amount)")
	fmt.Println("  sdk.TransferSpot(token, destination, amount)")
	fmt.Println("  sdk.TransferSpotToPerp(amount)")
	fmt.Println("  sdk.TransferPerpToSpot(amount)")
	fmt.Println("  sdk.SendAsset(token, amount, destination, opts)")
}
