// Trigger Orders Example
//
// Stop loss and take profit orders.
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

	mid, err := sdk.GetMid("BTC")
	if err != nil {
		log.Fatalf("Failed to get mid: %v", err)
	}
	fmt.Printf("BTC mid: $%.2f\n", mid)

	// Stop loss order (market) - triggers when price falls below stop price
	// No limit price means market order when triggered
	// result, _ := sdk.StopLoss("BTC", 0.001, mid*0.95, nil, nil)
	// fmt.Printf("Stop loss (market): %v\n", result)

	// Stop loss order (limit) - triggers and places limit order at limitPrice
	// limitPrice := mid * 0.94
	// result, _ := sdk.StopLoss("BTC", 0.001, mid*0.95, &limitPrice, nil)
	// fmt.Printf("Stop loss (limit): %v\n", result)

	// Take profit order (market) - triggers when price rises above trigger
	// result, _ := sdk.TakeProfit("BTC", 0.001, mid*1.05, nil, nil)
	// fmt.Printf("Take profit (market): %v\n", result)

	// Take profit order (limit)
	// limitPrice := mid * 1.06
	// result, _ := sdk.TakeProfit("BTC", 0.001, mid*1.05, &limitPrice, nil)
	// fmt.Printf("Take profit (limit): %v\n", result)

	// For buy-side stop/TP (e.g., closing a short position), use Side.BUY
	// side := hyperliquid.SideBuy
	// result, _ := sdk.StopLoss("BTC", 0.001, mid*1.05, nil, &side)

	fmt.Println("\nTrigger order methods available:")
	fmt.Println("  sdk.StopLoss(asset, size, triggerPrice, limitPrice, side)")
	fmt.Println("  sdk.TakeProfit(asset, size, triggerPrice, limitPrice, side)")
	fmt.Println("  sdk.PlaceTriggerOrder(TriggerOrder(...), grouping)")
	fmt.Println("\nNote: Omit limitPrice for market orders when triggered")
}
