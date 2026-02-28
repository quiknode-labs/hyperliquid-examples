// gRPC Streaming Example — High-Performance Real-Time Data
//
// Stream trades, orders, L2 book, L4 book, and blocks via gRPC.
// gRPC provides lower latency than WebSocket for high-frequency trading.
//
// gRPC is included with all QuickNode Hyperliquid endpoints — no add-on needed.
//
// Setup:
//     go build
//
// Usage:
//     export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
//     ./stream_grpc
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
		fmt.Println("gRPC Streaming Example")
		fmt.Println("============================================================")
		fmt.Println()
		fmt.Println("Usage:")
		fmt.Println("  export ENDPOINT='https://YOUR-ENDPOINT.quiknode.pro/TOKEN'")
		fmt.Println("  go run stream_grpc.go")
		fmt.Println()
		fmt.Println("gRPC is included with all QuickNode Hyperliquid endpoints.")
		os.Exit(1)
	}

	fmt.Println("============================================================")
	fmt.Println("gRPC Streaming Examples")
	fmt.Println("============================================================")
	fmt.Printf("Endpoint: %s...\n", truncate(endpoint, 50))
	fmt.Println()
	fmt.Println("This demo shows all gRPC streaming capabilities:")
	fmt.Println("  1. Trades — Real-time executed trades")
	fmt.Println("  2. L2 Book — Aggregated order book by price level")
	fmt.Println("  3. L4 Book — Individual orders (CRITICAL for trading)")
	fmt.Println("  4. Orders — Order lifecycle events")
	fmt.Println("  5. Blocks — Block data")
	fmt.Println()

	// Example 1: Stream Trades
	streamTradesExample(endpoint)

	// Example 2: Stream L2 Book
	streamL2BookExample(endpoint)

	fmt.Println()
	fmt.Println("============================================================")
	fmt.Println("All examples completed!")
	fmt.Println("============================================================")
}

func streamTradesExample(endpoint string) {
	fmt.Println()
	fmt.Println("============================================================")
	fmt.Println("EXAMPLE 1: Streaming Trades")
	fmt.Println("============================================================")

	stream := hyperliquid.NewGRPCStream(endpoint, nil)
	tradeCount := 0

	stream.Trades([]string{"BTC", "ETH"}, func(data map[string]any) {
		tradeCount++
		side := "BUY "
		if data["side"] == "A" {
			side = "SELL"
		}
		fmt.Printf("[%s] %s %s %s @ $%s\n",
			time.Now().Format("15:04:05.000"),
			side, data["sz"], data["coin"], data["px"])
	})

	fmt.Println("Subscribing to BTC and ETH trades...")
	fmt.Println("------------------------------------------------------------")

	if err := stream.Start(); err != nil {
		fmt.Printf("Failed to start stream: %v\n", err)
		return
	}

	time.Sleep(10 * time.Second)
	stream.Stop()
	fmt.Printf("Total trades received: %d\n", tradeCount)
}

func streamL2BookExample(endpoint string) {
	fmt.Println()
	fmt.Println("============================================================")
	fmt.Println("EXAMPLE 2: Streaming L2 Order Book (Aggregated)")
	fmt.Println("============================================================")
	fmt.Println()
	fmt.Println("L2 book aggregates orders at each price level.")
	fmt.Println("Use nSigFigs to control price aggregation precision.")
	fmt.Println()

	stream := hyperliquid.NewGRPCStream(endpoint, nil)
	updateCount := 0

	stream.L2Book("BTC", func(data map[string]any) {
		updateCount++
		if updateCount <= 3 {
			bids, _ := data["bids"].([]any)
			asks, _ := data["asks"].([]any)
			fmt.Printf("[%s] BTC L2 Book:\n", time.Now().Format("15:04:05.000"))
			if len(bids) > 0 {
				bid := bids[0].([]any)
				fmt.Printf("  Best Bid: $%s x %s\n", bid[0], bid[1])
			}
			if len(asks) > 0 {
				ask := asks[0].([]any)
				fmt.Printf("  Best Ask: $%s x %s\n", ask[0], ask[1])
			}
			fmt.Printf("  Levels: %d bids, %d asks\n\n", len(bids), len(asks))
		}
	}, hyperliquid.L2BookNSigFigs(5)) // nSigFigs=5 for full precision

	fmt.Println("Subscribing to BTC L2 book via gRPC (nSigFigs=5)...")
	fmt.Println("------------------------------------------------------------")

	if err := stream.Start(); err != nil {
		fmt.Printf("Failed to start stream: %v\n", err)
		return
	}

	time.Sleep(10 * time.Second)
	stream.Stop()
	fmt.Printf("Total L2 updates received: %d\n", updateCount)
}

func truncate(s string, n int) string {
	if len(s) <= n {
		return s
	}
	return s[:n]
}
