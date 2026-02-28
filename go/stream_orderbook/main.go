// Order Book Streaming Examples (gRPC)
//
// Shows L2 vs L4 order book streaming via gRPC.
//
// Setup:
//     go build
//
// Usage:
//     export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
//     ./stream_orderbook
package main

import (
	"fmt"
	"os"

	_ "github.com/quiknode-labs/raptor/hyperliquid-sdk/go/hyperliquid"
)

func main() {
	endpoint := os.Getenv("ENDPOINT")
	if endpoint == "" {
		endpoint = os.Getenv("QUICKNODE_ENDPOINT")
	}

	fmt.Println("============================================================")
	fmt.Println("Order Book Streaming Examples (gRPC)")
	fmt.Println("============================================================")
	if endpoint != "" {
		fmt.Printf("Endpoint: %s...\n", truncate(endpoint, 50))
	}
	fmt.Println()
	fmt.Println("============================================================")
	fmt.Println("L2 vs L4 ORDER BOOK COMPARISON")
	fmt.Println("============================================================")
	fmt.Println()
	fmt.Println("┌─────────────────────────────────────────────────────────────┐")
	fmt.Println("│                    L2 ORDER BOOK                            │")
	fmt.Println("├─────────────────────────────────────────────────────────────┤")
	fmt.Println("│ • Aggregated by price level                                 │")
	fmt.Println("│ • Shows total size at each price                            │")
	fmt.Println("│ • Available via gRPC (StreamL2Book)                         │")
	fmt.Println("│ • Lower bandwidth                                           │")
	fmt.Println("│ • Good for: Price monitoring, simple trading                │")
	fmt.Println("├─────────────────────────────────────────────────────────────┤")
	fmt.Println("│ Example:                                                    │")
	fmt.Println("│   Price: $95,000.00 | Total Size: 10.5 BTC                  │")
	fmt.Println("│   Price: $94,999.00 | Total Size: 5.2 BTC                   │")
	fmt.Println("└─────────────────────────────────────────────────────────────┘")
	fmt.Println()
	fmt.Println("┌─────────────────────────────────────────────────────────────┐")
	fmt.Println("│                    L4 ORDER BOOK                            │")
	fmt.Println("├─────────────────────────────────────────────────────────────┤")
	fmt.Println("│ • Individual orders with Order IDs                          │")
	fmt.Println("│ • Shows each order separately                               │")
	fmt.Println("│ • Available via gRPC only (StreamL4Book)                    │")
	fmt.Println("│ • Higher bandwidth, more data                               │")
	fmt.Println("│ • CRITICAL for: Market making, order flow analysis          │")
	fmt.Println("├─────────────────────────────────────────────────────────────┤")
	fmt.Println("│ Example:                                                    │")
	fmt.Println("│   OID: 123456 | $95,000.00 | 2.5 BTC                        │")
	fmt.Println("│   OID: 123457 | $95,000.00 | 3.0 BTC                        │")
	fmt.Println("│   OID: 123458 | $95,000.00 | 5.0 BTC                        │")
	fmt.Println("└─────────────────────────────────────────────────────────────┘")
	fmt.Println()
	fmt.Println("Usage:")
	fmt.Println()
	fmt.Println("  // L2 Order Book (aggregated)")
	fmt.Println("  stream.L2Book(\"BTC\", callback, 5)  // nSigFigs=5 for full precision")
	fmt.Println()
	fmt.Println("  // L4 Order Book (individual orders)")
	fmt.Println("  stream.L4Book(\"BTC\", callback)")
	fmt.Println()
	fmt.Println("See stream_l2_book.go and stream_l4_book.go for complete examples.")
}

func truncate(s string, n int) string {
	if len(s) <= n {
		return s
	}
	return s[:n]
}
