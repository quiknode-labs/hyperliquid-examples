// Cancel by Client Order ID (CLOID) Example
//
// Cancel an order using a client-provided order ID instead of the exchange OID.
// Useful when you track orders by your own IDs.
package main

import (
	"fmt"

	_ "github.com/quiknode-labs/raptor/hyperliquid-sdk/go/hyperliquid"
)

func main() {
	// Note: CLOIDs are hex strings you provide when placing orders
	// This example shows the CancelByCloid API

	// Cancel by client order ID
	// sdk.CancelByCloid("0x1234567890abcdef...", "BTC")

	fmt.Println("CancelByCloid() cancels orders by your custom client order ID")
	fmt.Println("Usage: sdk.CancelByCloid(cloid, asset)")
}
