// Vaults Example
//
// Deposit and withdraw from Hyperliquid vaults.
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

	// Example vault address (HLP vault)
	// HLP_VAULT := "0xdfc24b077bc1425ad1dea75bcb6f8158e10df303"

	// Deposit to vault
	// result, _ := sdk.VaultDeposit(HLP_VAULT, 100.0)
	// fmt.Printf("Vault deposit: %v\n", result)

	// Withdraw from vault
	// result, _ := sdk.VaultWithdraw(HLP_VAULT, 50.0)
	// fmt.Printf("Vault withdraw: %v\n", result)

	fmt.Println("Vault methods available:")
	fmt.Println("  sdk.VaultDeposit(vaultAddress, amount)")
	fmt.Println("  sdk.VaultWithdraw(vaultAddress, amount)")
}
