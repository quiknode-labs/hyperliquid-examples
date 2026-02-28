// Schedule Cancel Example (Dead Man's Switch)
//
// Schedule automatic cancellation of all orders after a delay.
// If you don't send another schedule_cancel before the time expires,
// all your orders are cancelled. Useful as a safety mechanism.
//
// NOTE: Requires $1M trading volume on your account to use this feature.
package main

import (
	"fmt"

	_ "github.com/quiknode-labs/raptor/hyperliquid-sdk/go/hyperliquid"
)

func main() {
	// sdk, _ := hyperliquid.New("", hyperliquid.WithPrivateKey(privateKey))

	// Schedule cancel all orders in 60 seconds
	// cancelTime := time.Now().UnixMilli() + 60000 // 60 seconds from now
	// result, _ := sdk.ScheduleCancel(&cancelTime)
	// fmt.Printf("Scheduled cancel at %d: %v\n", cancelTime, result)

	// To cancel the scheduled cancel (keep orders alive):
	// result, _ := sdk.ScheduleCancel(nil)
	// fmt.Printf("Cancelled scheduled cancel: %v\n", result)

	fmt.Println("Schedule cancel methods available:")
	fmt.Println("  sdk.ScheduleCancel(&timeMs)  // Schedule cancel at timestamp")
	fmt.Println("  sdk.ScheduleCancel(nil)      // Cancel the scheduled cancel")
	fmt.Println("\nNOTE: Requires $1M trading volume on your account")
}
