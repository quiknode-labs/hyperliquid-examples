// Full Demo Example
//
// Comprehensive demo showing all SDK capabilities.
//
// Setup:
//     go build
//
// Usage:
//     export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
//     export PRIVATE_KEY="0x..."
//     ./full_demo
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
	privateKey := os.Getenv("PRIVATE_KEY")

	if endpoint == "" {
		fmt.Println("Set ENDPOINT environment variable")
		os.Exit(1)
	}

	fmt.Println()
	fmt.Println("************************************************************")
	fmt.Println("  HYPERLIQUID SDK - FULL DEMO")
	fmt.Println("************************************************************")
	fmt.Printf("\nEndpoint: %s...\n", truncate(endpoint, 50))

	var sdk *hyperliquid.SDK
	var err error
	if privateKey != "" {
		sdk, err = hyperliquid.New(endpoint, hyperliquid.WithPrivateKey(privateKey))
	} else {
		sdk, err = hyperliquid.New(endpoint)
	}
	if err != nil {
		log.Fatalf("Failed to create SDK: %v", err)
	}

	// ==========================================================================
	// INFO API
	// ==========================================================================
	fmt.Println()
	fmt.Println("============================================================")
	fmt.Println("  INFO API")
	fmt.Println("============================================================")

	info := sdk.Info()

	// Market Prices
	fmt.Println("\n--- Market Prices ---")
	mids, err := info.AllMids()
	if err != nil {
		log.Printf("Failed to get mids: %v", err)
	} else {
		fmt.Printf("Total markets: %d\n", len(mids))
		coins := []string{"BTC", "ETH", "SOL", "DOGE"}
		for _, coin := range coins {
			if price, ok := mids[coin]; ok {
				fmt.Printf("  %s: $%s\n", coin, price)
			}
		}
	}

	// Order Book
	fmt.Println("\n--- Order Book ---")
	book, err := info.L2Book("BTC")
	if err != nil {
		log.Printf("Failed to get L2 book: %v", err)
	} else {
		levels, _ := book["levels"].([]any)
		if len(levels) >= 2 {
			bids, _ := levels[0].([]any)
			if len(bids) > 0 {
				bid := bids[0].(map[string]any)
				fmt.Printf("  Best Bid: %s @ $%s\n", bid["sz"], bid["px"])
			}
		}
	}

	// ==========================================================================
	// HYPERCORE API
	// ==========================================================================
	fmt.Println()
	fmt.Println("============================================================")
	fmt.Println("  HYPERCORE API")
	fmt.Println("============================================================")

	core := sdk.Core()

	fmt.Println("\n--- Block Info ---")
	blockNum, err := core.LatestBlockNumber()
	if err != nil {
		log.Printf("Failed to get block: %v", err)
	} else {
		fmt.Printf("Latest block: %d\n", blockNum)
	}

	fmt.Println("\n--- Recent Trades ---")
	trades, err := core.LatestTrades(3, "")
	if err != nil {
		log.Printf("Failed to get trades: %v", err)
	} else {
		for _, trade := range trades {
			side := "BUY"
			if trade["side"] == "A" {
				side = "SELL"
			}
			fmt.Printf("  %s %s %s @ $%s\n", side, trade["sz"], trade["coin"], trade["px"])
		}
	}

	// ==========================================================================
	// EVM API
	// ==========================================================================
	fmt.Println()
	fmt.Println("============================================================")
	fmt.Println("  EVM API")
	fmt.Println("============================================================")

	evm := sdk.EVM()

	fmt.Println("\n--- Chain Info ---")
	chainID, _ := evm.ChainID()
	evmBlock, _ := evm.BlockNumber()
	gasPrice, _ := evm.GasPrice()
	fmt.Printf("Chain ID: %d\n", chainID)
	fmt.Printf("Block: %d\n", evmBlock)
	fmt.Printf("Gas Price: %.2f gwei\n", float64(gasPrice)/1e9)

	// ==========================================================================
	// TRADING (if private key provided)
	// ==========================================================================
	if privateKey != "" {
		fmt.Println()
		fmt.Println("============================================================")
		fmt.Println("  TRADING")
		fmt.Println("============================================================")
		fmt.Printf("\nWallet: %s\n", sdk.Address())

		// Quick roundtrip trade
		fmt.Println("\n--- Quick Roundtrip ---")
		buy, err := sdk.MarketBuy("BTC", hyperliquid.WithNotional(11))
		if err != nil {
			log.Printf("Buy failed: %v", err)
		} else {
			fmt.Printf("Bought: %s BTC\n", buy.FilledSize)
			time.Sleep(500 * time.Millisecond)

			sell, err := sdk.MarketSell("BTC", hyperliquid.WithSize(buy.FilledSize))
			if err != nil {
				log.Printf("Sell failed: %v", err)
			} else {
				fmt.Printf("Sold: %s BTC\n", sell.FilledSize)
			}
		}
	}

	fmt.Println()
	fmt.Println("============================================================")
	fmt.Println("  DEMO COMPLETE")
	fmt.Println("============================================================")
}

func truncate(s string, n int) string {
	if len(s) <= n {
		return s
	}
	return s[:n]
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
