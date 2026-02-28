// WebSocket Streaming — Complete Reference
//
// Shows all available WebSocket subscription types.
//
// Setup:
//     go build
//
// Usage:
//     export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"
//     ./stream_websocket_all
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
	fmt.Println("WebSocket Streaming — Complete Reference")
	fmt.Println("============================================================")
	if endpoint != "" {
		fmt.Printf("Endpoint: %s...\n", truncate(endpoint, 50))
	}
	fmt.Println()
	fmt.Println()
	fmt.Println("============================================================")
	fmt.Println("WEBSOCKET SUBSCRIPTION REFERENCE")
	fmt.Println("============================================================")
	fmt.Println()
	fmt.Println("┌────────────────────────┬────────────────────────────────────────┐")
	fmt.Println("│ Method                 │ Description                            │")
	fmt.Println("├────────────────────────┼────────────────────────────────────────┤")
	fmt.Println("│ MARKET DATA            │                                        │")
	fmt.Println("│ Trades(coins, cb)      │ Executed trades                        │")
	fmt.Println("│ BookUpdates(coins,cb)  │ Order book deltas                      │")
	fmt.Println("│ L2Book(coin, cb)       │ Full L2 order book                     │")
	fmt.Println("│ AllMids(cb)            │ All asset mid prices                   │")
	fmt.Println("│ Candle(coin,int,cb)    │ OHLCV candles (1m,5m,15m,1h,4h,1d)     │")
	fmt.Println("│ BBO(coin, cb)          │ Best bid/offer                         │")
	fmt.Println("├────────────────────────┼────────────────────────────────────────┤")
	fmt.Println("│ ORDER DATA             │                                        │")
	fmt.Println("│ Orders(coins, cb)      │ Order lifecycle events                 │")
	fmt.Println("│ OpenOrders(user, cb)   │ User's open orders                     │")
	fmt.Println("│ OrderUpdates(user, cb) │ User's order changes                   │")
	fmt.Println("├────────────────────────┼────────────────────────────────────────┤")
	fmt.Println("│ USER DATA              │                                        │")
	fmt.Println("│ Events(cb)             │ Balance changes, transfers             │")
	fmt.Println("│ UserEvents(user, cb)   │ User-specific events                   │")
	fmt.Println("│ UserFills(user, cb)    │ User's filled trades                   │")
	fmt.Println("│ UserFundings(user, cb) │ User's funding payments                │")
	fmt.Println("├────────────────────────┼────────────────────────────────────────┤")
	fmt.Println("│ TWAP                   │                                        │")
	fmt.Println("│ Twap(coins, cb)        │ TWAP execution data                    │")
	fmt.Println("│ TwapStates(user, cb)   │ User's TWAP states                     │")
	fmt.Println("├────────────────────────┼────────────────────────────────────────┤")
	fmt.Println("│ HYPERCORE              │                                        │")
	fmt.Println("│ WriterActions(cb)      │ HyperCore <-> HyperEVM transfers       │")
	fmt.Println("└────────────────────────┴────────────────────────────────────────┘")
	fmt.Println()
	fmt.Println("Example:")
	fmt.Println()
	fmt.Println("  stream := hyperliquid.NewStream(endpoint, nil)")
	fmt.Println("  stream.Trades([]string{\"BTC\", \"ETH\"}, func(data map[string]any) {")
	fmt.Println("      fmt.Println(data)")
	fmt.Println("  })")
	fmt.Println("  stream.Start()")
	fmt.Println()
}

func truncate(s string, n int) string {
	if len(s) <= n {
		return s
	}
	return s[:n]
}
