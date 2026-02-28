// Historical Candles Example
//
// Shows how to fetch historical candlestick (OHLCV) data.
//
// Note: candleSnapshot may not be available on all QuickNode endpoints.
// Check the QuickNode docs for method availability.
//
// Setup:
//     go build
//
// Usage:
//     export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
//     ./info_candles
package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"time"

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
	info := sdk.Info()

	fmt.Println("==================================================")
	fmt.Println("Historical Candles")
	fmt.Println("==================================================")

	// Last 24 hours
	now := time.Now().UnixMilli()
	dayAgo := now - (24 * 60 * 60 * 1000)

	// Fetch BTC 1-hour candles
	fmt.Println("\n1. BTC 1-Hour Candles (last 24h):")
	candles, err := info.Candles("BTC", "1h", dayAgo, now)
	if err != nil {
		fmt.Printf("   Error: %v\n", err)
		fmt.Println("   Note: candleSnapshot may not be available on this endpoint")
	} else {
		fmt.Printf("   Retrieved %d candles\n", len(candles))
		start := len(candles) - 3
		if start < 0 {
			start = 0
		}
		for _, c := range candles[start:] {
			candle := c.(map[string]any)
			fmt.Printf("   O:%s H:%s L:%s C:%s\n", candle["o"], candle["h"], candle["l"], candle["c"])
		}
	}

	// Predicted funding rates (supported on QuickNode)
	fmt.Println("\n2. Predicted Funding Rates:")
	fundings, err := info.PredictedFundings()
	if err != nil {
		fmt.Printf("   Error: %v\n", err)
	} else {
		fmt.Printf("   %d assets with funding rates:\n", len(fundings))
		count := 0
		for _, item := range fundings {
			if count >= 5 {
				break
			}
			arr, ok := item.([]any)
			if !ok || len(arr) < 2 {
				continue
			}
			coin, _ := arr[0].(string)
			sources, _ := arr[1].([]any)
			if len(sources) == 0 {
				continue
			}
			for _, src := range sources {
				srcArr, ok := src.([]any)
				if !ok || len(srcArr) < 2 {
					continue
				}
				if srcArr[0] == "HlPerp" {
					rateInfo, _ := srcArr[1].(map[string]any)
					rate := parseFloat(rateInfo["fundingRate"]) * 100
					fmt.Printf("   %s: %.4f%%\n", coin, rate)
					count++
					break
				}
			}
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
