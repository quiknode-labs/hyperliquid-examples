// Market Data Example
//
// Shows how to query market metadata, prices, order book, and recent trades.
//
// The SDK handles all Info API methods automatically.
//
// Setup:
//     go build
//
// Usage:
//     export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
//     ./info_market_data
package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"strconv"

	"github.com/quiknode-labs/raptor/hyperliquid-sdk/go/hyperliquid"
)

func main() {
	endpoint := os.Getenv("ENDPOINT")
	if endpoint == "" {
		endpoint = os.Getenv("QUICKNODE_ENDPOINT")
	}
	if endpoint == "" {
		fmt.Println("Set ENDPOINT environment variable")
		fmt.Println("Example: export ENDPOINT='https://your-endpoint.hype-mainnet.quiknode.pro/TOKEN'")
		os.Exit(1)
	}

	sdk, err := hyperliquid.New(endpoint)
	if err != nil {
		log.Fatalf("Failed to create SDK: %v", err)
	}
	info := sdk.Info()

	fmt.Println("==================================================")
	fmt.Println("Market Data (Info API)")
	fmt.Println("==================================================")

	// Exchange metadata
	fmt.Println("\n1. Exchange Metadata:")
	meta, err := info.Meta()
	if err != nil {
		fmt.Printf("   (meta not available: %v)\n", err)
	} else {
		universe, _ := meta["universe"].([]any)
		fmt.Printf("   Perp Markets: %d\n", len(universe))
		for i, asset := range universe {
			if i >= 5 {
				break
			}
			a := asset.(map[string]any)
			fmt.Printf("   - %s: max leverage %vx\n", a["name"], a["maxLeverage"])
		}
	}

	// Spot metadata
	fmt.Println("\n2. Spot Metadata:")
	spot, err := info.SpotMeta()
	if err != nil {
		fmt.Printf("   (spot_meta not available: %v)\n", err)
	} else {
		tokens, _ := spot["tokens"].([]any)
		fmt.Printf("   Spot Tokens: %d\n", len(tokens))
	}

	// Exchange status
	fmt.Println("\n3. Exchange Status:")
	status, err := info.ExchangeStatus()
	if err != nil {
		fmt.Printf("   (exchange_status not available: %v)\n", err)
	} else {
		jsonStatus, _ := json.Marshal(status)
		fmt.Printf("   %s\n", jsonStatus)
	}

	// All mid prices
	fmt.Println("\n4. Mid Prices:")
	mids, err := info.AllMids()
	if err != nil {
		fmt.Printf("   (allMids not available: %v)\n", err)
	} else {
		fmt.Printf("   BTC: $%.2f\n", parseFloat(mids["BTC"]))
	}

	// Order book
	fmt.Println("\n5. Order Book (BTC):")
	book, err := info.L2Book("BTC")
	if err != nil {
		fmt.Printf("   (l2_book not available: %v)\n", err)
	} else {
		levels, _ := book["levels"].([]any)
		if len(levels) >= 2 {
			bids, _ := levels[0].([]any)
			asks, _ := levels[1].([]any)
			if len(bids) > 0 && len(asks) > 0 {
				bestBid := bids[0].(map[string]any)
				bestAsk := asks[0].(map[string]any)
				bidPx := parseFloat(bestBid["px"])
				askPx := parseFloat(bestAsk["px"])
				spread := askPx - bidPx
				fmt.Printf("   Best Bid: $%.2f\n", bidPx)
				fmt.Printf("   Best Ask: $%.2f\n", askPx)
				fmt.Printf("   Spread: $%.2f\n", spread)
			}
		}
	}

	// Recent trades
	fmt.Println("\n6. Recent Trades (BTC):")
	trades, err := info.RecentTrades("BTC")
	if err != nil {
		fmt.Printf("   (recent_trades not available: %v)\n", err)
	} else {
		for i, t := range trades {
			if i >= 3 {
				break
			}
			trade := t.(map[string]any)
			side := "BUY"
			if trade["side"] == "A" {
				side = "SELL"
			}
			fmt.Printf("   %s %s @ $%.2f\n", side, trade["sz"], parseFloat(trade["px"]))
		}
	}

	fmt.Println("\n==================================================")
	fmt.Println("Done!")
}

func parseFloat(v any) float64 {
	switch val := v.(type) {
	case string:
		f, _ := strconv.ParseFloat(val, 64)
		return f
	case float64:
		return val
	default:
		return 0
	}
}
