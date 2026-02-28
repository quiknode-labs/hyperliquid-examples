// WebSocket Streaming Example — Real-Time HyperCore Data
//
// Stream trades, orders, book updates, events, and TWAP via WebSocket.
// These are the data streams available on QuickNode endpoints.
//
// Setup:
//     go build
//
// Usage:
//     export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
//     ./stream_trades
package main

import (
	"fmt"
	"os"
	"time"

	"github.com/quiknode-labs/raptor/hyperliquid-sdk/go/hyperliquid"
)

func main() {
	endpoint := os.Getenv("ENDPOINT")
	if endpoint == "" {
		endpoint = os.Getenv("QUICKNODE_ENDPOINT")
	}
	if endpoint == "" {
		fmt.Println("WebSocket Streaming Example")
		fmt.Println("============================================================")
		fmt.Println()
		fmt.Println("Usage:")
		fmt.Println("  export ENDPOINT='https://YOUR-ENDPOINT.quiknode.pro/TOKEN'")
		fmt.Println("  go run stream_trades.go")
		os.Exit(1)
	}

	fmt.Println("============================================================")
	fmt.Println("WebSocket Streaming Examples (QuickNode)")
	fmt.Println("============================================================")
	fmt.Printf("Endpoint: %s...\n", truncate(endpoint, 50))
	fmt.Println()
	fmt.Println("This demo shows QuickNode WebSocket streaming capabilities:")
	fmt.Println("  1. Trades - Real-time executed trades")
	fmt.Println("  2. Orders - Order lifecycle events")
	fmt.Println("  3. Book Updates - Incremental order book changes")
	fmt.Println("  4. Events - Balance changes, transfers, etc.")
	fmt.Println("  5. Multi-stream - Multiple subscriptions")
	fmt.Println()

	// Example 1: Stream Trades
	fmt.Println()
	fmt.Println("============================================================")
	fmt.Println("EXAMPLE 1: Streaming Trades")
	fmt.Println("============================================================")
	fmt.Println("Subscribing to BTC and ETH trades...")
	fmt.Println("------------------------------------------------------------")

	stream := hyperliquid.NewStream(endpoint, nil)
	tradeCount := 0

	stream.Trades([]string{"BTC", "ETH"}, func(data map[string]any) {
		tradeCount++
		block, _ := data["block"].(map[string]any)
		events, _ := block["events"].([]any)
		for _, event := range events {
			if arr, ok := event.([]any); ok && len(arr) >= 2 {
				trade, _ := arr[1].(map[string]any)
				side := "BUY "
				if trade["side"] == "A" {
					side = "SELL"
				}
				fmt.Printf("[%s] %s %s %s @ $%s\n",
					time.Now().Format("15:04:05.000"),
					side, trade["sz"], trade["coin"], trade["px"])
			}
		}
	})

	if err := stream.Start(); err != nil {
		fmt.Printf("Failed to start stream: %v\n", err)
		return
	}

	// Run for 10 seconds
	time.Sleep(10 * time.Second)
	stream.Stop()

	fmt.Printf("\nTotal trades received: %d\n", tradeCount)

	// Show available streams
	fmt.Println()
	fmt.Println("============================================================")
	fmt.Println("AVAILABLE QUICKNODE WEBSOCKET STREAMS")
	fmt.Println("============================================================")
	fmt.Println()
	fmt.Println("HyperCore Data Streams:")
	fmt.Println()
	fmt.Println("  stream.Trades(coins, callback)")
	fmt.Println("    - Executed trades with price, size, direction")
	fmt.Println()
	fmt.Println("  stream.Orders(coins, callback)")
	fmt.Println("    - Order lifecycle: open, filled, triggered, canceled")
	fmt.Println()
	fmt.Println("  stream.BookUpdates(coins, callback)")
	fmt.Println("    - Incremental order book changes (deltas)")
	fmt.Println()
	fmt.Println("  stream.Events(callback)")
	fmt.Println("    - Balance changes, transfers, deposits, withdrawals")
	fmt.Println()
	fmt.Println("For L2/L4 Order Books:")
	fmt.Println("  Use gRPC streaming (see stream_grpc.go)")
	fmt.Println()
}

func truncate(s string, n int) string {
	if len(s) <= n {
		return s
	}
	return s[:n]
}
