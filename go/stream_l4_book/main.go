// L4 Order Book Streaming — Individual Orders
//
// L4 book shows EVERY individual order in the book.
// This is CRITICAL for market making and order flow analysis.
//
// L4 book is CRITICAL for:
// - Market making: See exact order sizes and queue position
// - Order flow analysis: Detect large orders and icebergs
// - Optimal execution: Know exactly what you're crossing
//
// Setup:
//     go build
//
// Usage:
//     export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
//     ./stream_l4_book
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
		fmt.Println("L4 Order Book Streaming Example")
		fmt.Println("============================================================")
		fmt.Println()
		fmt.Println("Usage:")
		fmt.Println("  export ENDPOINT='https://YOUR-ENDPOINT.quiknode.pro/TOKEN'")
		fmt.Println("  go run stream_l4_book.go")
		os.Exit(1)
	}

	fmt.Println("============================================================")
	fmt.Println("L4 ORDER BOOK STREAMING (Individual Orders)")
	fmt.Println("============================================================")
	fmt.Printf("Endpoint: %s...\n", truncate(endpoint, 50))
	fmt.Println()
	fmt.Println("L4 book shows EVERY individual order in the book.")
	fmt.Println("This is critical for market making and order flow analysis.")
	fmt.Println()

	stream := hyperliquid.NewGRPCStream(endpoint, nil)
	updateCount := 0

	stream.L4Book("BTC", func(data map[string]any) {
		updateCount++
		if updateCount <= 3 {
			updateType := data["type"]
			bids, _ := data["bids"].([]any)
			asks, _ := data["asks"].([]any)

			fmt.Printf("\n[%s] BTC L4 Book (%s) #%d:\n", time.Now().Format("15:04:05.000"), updateType, updateCount)

			if updateType == "snapshot" {
				fmt.Printf("  Total: %d bids, %d asks\n", len(bids), len(asks))
				fmt.Println("  TOP BIDS:")
				for i := 0; i < 3 && i < len(bids); i++ {
					bid, _ := bids[i].(map[string]any)
					fmt.Printf("    [%d] $%s x %s (oid: %v)\n", i+1, bid["limit_px"], bid["sz"], bid["oid"])
				}
				fmt.Println("  TOP ASKS:")
				for i := 0; i < 3 && i < len(asks); i++ {
					ask, _ := asks[i].(map[string]any)
					fmt.Printf("    [%d] $%s x %s (oid: %v)\n", i+1, ask["limit_px"], ask["sz"], ask["oid"])
				}
			} else {
				fmt.Println("  (incremental update)")
			}
			fmt.Println()
		}
	})

	fmt.Println("Subscribing to BTC L4 order book (individual orders)...")
	fmt.Println("------------------------------------------------------------")

	if err := stream.Start(); err != nil {
		fmt.Printf("Failed to start stream: %v\n", err)
		return
	}

	time.Sleep(15 * time.Second)
	stream.Stop()

	fmt.Printf("Total L4 updates received: %d\n", updateCount)
}

func truncate(s string, n int) string {
	if len(s) <= n {
		return s
	}
	return s[:n]
}
