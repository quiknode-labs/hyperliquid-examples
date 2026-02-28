// HyperEVM Example
//
// Shows how to use standard Ethereum JSON-RPC calls on Hyperliquid's EVM chain.
//
// Setup:
//     go build
//
// Usage:
//     export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
//     ./evm_basics
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
	if endpoint == "" {
		fmt.Println("Set ENDPOINT environment variable")
		os.Exit(1)
	}

	sdk, err := hyperliquid.New(endpoint)
	if err != nil {
		log.Fatalf("Failed to create SDK: %v", err)
	}
	evm := sdk.EVM()

	fmt.Println("==================================================")
	fmt.Println("HyperEVM (Ethereum JSON-RPC)")
	fmt.Println("==================================================")

	// Chain info
	fmt.Println("\n1. Chain Info:")
	chainID, err := evm.ChainID()
	if err != nil {
		log.Printf("Failed to get chain ID: %v", err)
	} else {
		fmt.Printf("   Chain ID: %d\n", chainID)
	}

	blockNum, err := evm.BlockNumber()
	if err != nil {
		log.Printf("Failed to get block number: %v", err)
	} else {
		fmt.Printf("   Block: %d\n", blockNum)
	}

	gasPrice, err := evm.GasPrice()
	if err != nil {
		log.Printf("Failed to get gas price: %v", err)
	} else {
		fmt.Printf("   Gas Price: %.2f gwei\n", float64(gasPrice)/1e9)
	}

	// Latest block
	fmt.Println("\n2. Latest Block:")
	block, err := evm.GetBlockByNumber("latest", false)
	if err != nil {
		log.Printf("Failed to get block: %v", err)
	} else if block != nil {
		hash, _ := block["hash"].(string)
		txs, _ := block["transactions"].([]any)
		if len(hash) > 20 {
			hash = hash[:20]
		}
		fmt.Printf("   Hash: %s...\n", hash)
		fmt.Printf("   Txs: %d\n", len(txs))
	}

	// Check balance (returns hex string, need to parse)
	fmt.Println("\n3. Balance Check:")
	addr := "0x0000000000000000000000000000000000000000"
	balanceHex, err := evm.GetBalance(addr, "latest")
	if err != nil {
		log.Printf("Failed to get balance: %v", err)
	} else {
		fmt.Printf("   %s...: %s (hex)\n", addr[:12], balanceHex)
	}

	fmt.Println("\n==================================================")
	fmt.Println("Done!")
	fmt.Println("\nFor debug/trace APIs, use: new EVM(endpoint, { debug: true })")
}
