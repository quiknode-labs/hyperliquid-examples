// L2 Order Book Streaming — Aggregated Price Levels
//
// L2 order book shows total size at each price level (aggregated).
// Available via both WebSocket and gRPC.
//
// Use L2 for:
// - Price monitoring
// - Basic trading strategies
// - Lower bandwidth requirements
//
// Use L4 (gRPC only) when you need:
// - Individual order IDs
// - Queue position tracking
// - Order flow analysis
//
// Setup:
//     go build
//
// Usage:
//     export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
//     ./stream_l2_book
package main

import (
	"fmt"
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
		fmt.Println("L2 Order Book Streaming Example")
		fmt.Println("============================================================")
		fmt.Println()
		fmt.Println("Usage:")
		fmt.Println("  export ENDPOINT='https://YOUR-ENDPOINT.quiknode.pro/TOKEN'")
		fmt.Println("  go run stream_l2_book.go")
		os.Exit(1)
	}

	fmt.Println("============================================================")
	fmt.Println("L2 ORDER BOOK STREAMING")
	fmt.Println("============================================================")
	fmt.Printf("Endpoint: %s...\n", truncate(endpoint, 50))

	// Show comparison
	fmt.Println()
	fmt.Println("============================================================")
	fmt.Println("COMPARISON: gRPC vs WebSocket")
	fmt.Println("============================================================")
	fmt.Println()
	fmt.Println("┌─────────────────────────────────────────────────────────────┐")
	fmt.Println("│                      L2 VIA gRPC                            │")
	fmt.Println("├─────────────────────────────────────────────────────────────┤")
	fmt.Println("│ • Lower latency                                             │")
	fmt.Println("│ • nSigFigs parameter for aggregation control                │")
	fmt.Println("│ • Best for: HFT, latency-sensitive apps                     │")
	fmt.Println("│ • Port: 10000                                               │")
	fmt.Println("└─────────────────────────────────────────────────────────────┘")
	fmt.Println()
	fmt.Println("┌─────────────────────────────────────────────────────────────┐")
	fmt.Println("│                    L2 VIA WebSocket                         │")
	fmt.Println("├─────────────────────────────────────────────────────────────┤")
	fmt.Println("│ • Standard WebSocket (443)                                  │")
	fmt.Println("│ • Works in browsers                                         │")
	fmt.Println("│ • More subscription types available                         │")
	fmt.Println("│ • Best for: Web apps, general use                           │")
	fmt.Println("└─────────────────────────────────────────────────────────────┘")
	fmt.Println()

	// Stream L2 via gRPC
	fmt.Println()
	fmt.Println("============================================================")
	fmt.Println("L2 ORDER BOOK via gRPC")
	fmt.Println("============================================================")
	fmt.Println()
	fmt.Println("gRPC provides lower latency than WebSocket.")
	fmt.Println("nSigFigs controls price aggregation (3-5).")
	fmt.Println()

	stream := hyperliquid.NewGRPCStream(endpoint, nil)
	updateCount := 0

	stream.L2Book("BTC", func(data map[string]any) {
		updateCount++
		if updateCount <= 5 {
			bids, _ := data["bids"].([]any)
			asks, _ := data["asks"].([]any)

			fmt.Printf("\n[%s] BTC L2 Book (gRPC) #%d\n", time.Now().Format("15:04:05.000"), updateCount)
			fmt.Println("--------------------------------------------------")

			if len(bids) > 0 && len(asks) > 0 {
				bid := bids[0].([]any)
				ask := asks[0].([]any)
				bidPx := parseFloat(bid[0])
				askPx := parseFloat(ask[0])
				spread := askPx - bidPx

				fmt.Printf("  Best Bid: $%.2f x %s\n", bidPx, bid[1])
				fmt.Printf("  Best Ask: $%.2f x %s\n", askPx, ask[1])
				fmt.Printf("  Spread:   $%.2f\n", spread)
				fmt.Printf("  Levels:   %d bids, %d asks\n", len(bids), len(asks))
			}
		}
	}, hyperliquid.L2BookNSigFigs(5))

	fmt.Println("Subscribing to BTC L2 book via gRPC (nSigFigs=5)...")
	fmt.Println("------------------------------------------------------------")

	if err := stream.Start(); err != nil {
		fmt.Printf("Failed to start stream: %v\n", err)
		return
	}

	time.Sleep(15 * time.Second)
	stream.Stop()

	fmt.Printf("\nReceived %d L2 updates via gRPC\n", updateCount)

	fmt.Println()
	fmt.Println("============================================================")
	fmt.Println("All L2 examples completed!")
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
