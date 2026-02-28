// Round Trip Example
//
// Complete trade cycle: buy then sell to end up flat.
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

	// Buy $11 worth of BTC
	fmt.Println("Buying BTC...")
	buy, err := sdk.MarketBuy("BTC", hyperliquid.WithNotional(11))
	if err != nil {
		log.Fatalf("Failed to buy: %v", err)
	}
	filledSize := buy.FilledSize
	if filledSize == "" {
		filledSize = buy.Size
	}
	fmt.Printf("  Bought: %s BTC\n", filledSize)
	fmt.Printf("  Status: %s\n", buy.Status)

	// Sell the same amount
	fmt.Println("Selling BTC...")
	sell, err := sdk.MarketSell("BTC", hyperliquid.WithSize(filledSize))
	if err != nil {
		log.Fatalf("Failed to sell: %v", err)
	}
	soldSize := sell.FilledSize
	if soldSize == "" {
		soldSize = sell.Size
	}
	fmt.Printf("  Sold: %s BTC\n", soldSize)
	fmt.Printf("  Status: %s\n", sell.Status)

	fmt.Println("Done! Position should be flat.")
}
