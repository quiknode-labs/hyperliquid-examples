// Market Order Example
//
// Place a market order that executes immediately at best available price.
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

	// Market buy by notional ($11 worth of BTC - minimum is $10)
	order, err := sdk.MarketBuy("BTC", hyperliquid.WithNotional(11))
	if err != nil {
		log.Fatalf("Failed to place order: %v", err)
	}
	fmt.Printf("Market buy: %v\n", order)
	fmt.Printf("  Status: %s\n", order.Status)
	fmt.Printf("  OID: %d\n", order.OID)

	// Market buy by notional ($10 worth of ETH)
	// order, _ := sdk.MarketBuy("ETH", hyperliquid.WithNotional(10))

	// Market sell
	// order, _ := sdk.MarketSell("BTC", hyperliquid.WithSize(0.0001))
}
