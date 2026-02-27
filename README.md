# Hyperliquid Examples

> **Community Examples by [QuickNode](https://quicknode.com)** — Not affiliated with Hyperliquid Foundation.

Examples using the [Hyperliquid SDK](https://github.com/quiknode-labs/hyperliquid-sdk) for trading on Hyperliquid.

## Quick Start

### Python

```bash
# Install the SDK
pip install hyperliquid-sdk

# Set your private key (for trading examples)
export PRIVATE_KEY="0x..."

# Set your endpoint (for data examples)
export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"

# Run any example
cd python
python market_order.py
```

### TypeScript (Coming Soon)

```bash
npm install hyperliquid-sdk
cd typescript
npx ts-node market_order.ts
```

### Rust (Coming Soon)

```bash
cd rust
cargo run --example market_order
```

## Python Examples

### Trading — Order Placement
| Example | Description |
|---------|-------------|
| [market_order.py](python/market_order.py) | Market buy/sell that executes immediately |
| [place_order.py](python/place_order.py) | Limit order that rests on the book |
| [fluent_builder.py](python/fluent_builder.py) | Power user fluent API for orders |
| [hip3_order.py](python/hip3_order.py) | Trade HIP-3 markets (community perps) |

### Trading — Order Management
| Example | Description |
|---------|-------------|
| [cancel_order.py](python/cancel_order.py) | Cancel an order by OID |
| [cancel_by_cloid.py](python/cancel_by_cloid.py) | Cancel by client order ID |
| [cancel_all.py](python/cancel_all.py) | Cancel all open orders |
| [schedule_cancel.py](python/schedule_cancel.py) | Dead-man's switch auto-cancel |
| [modify_order.py](python/modify_order.py) | Modify a resting order |

### Trading — Position Management
| Example | Description |
|---------|-------------|
| [close_position.py](python/close_position.py) | Close a position completely |
| [roundtrip.py](python/roundtrip.py) | Buy then sell (complete cycle) |

### Info API — Market Data
| Example | Description |
|---------|-------------|
| [info_market_data.py](python/info_market_data.py) | Mid prices, order book, recent trades |
| [info_user_data.py](python/info_user_data.py) | Account state, positions, orders |
| [info_candles.py](python/info_candles.py) | OHLCV candlestick data |
| [info_vaults.py](python/info_vaults.py) | Vault summaries and details |
| [info_batch_queries.py](python/info_batch_queries.py) | Batch queries for multiple users |

### HyperCore API — Block Data
| Example | Description |
|---------|-------------|
| [hypercore_blocks.py](python/hypercore_blocks.py) | Blocks, trades, and order events |

### HyperEVM — Ethereum JSON-RPC
| Example | Description |
|---------|-------------|
| [evm_basics.py](python/evm_basics.py) | Chain ID, blocks, balances |

### Real-Time Streaming
| Example | Description |
|---------|-------------|
| [stream_trades.py](python/stream_trades.py) | WebSocket streaming basics (trades, L2 book, all mids, BBO) |
| [stream_grpc.py](python/stream_grpc.py) | gRPC streaming basics (trades, L2/L4 book, blocks) |
| [stream_orderbook.py](python/stream_orderbook.py) | L2 vs L4 order book comparison |
| [stream_l4_book.py](python/stream_l4_book.py) | **L4 order book (individual orders) — CRITICAL** |
| [stream_l2_book.py](python/stream_l2_book.py) | L2 order book via gRPC and WebSocket |
| [stream_websocket_all.py](python/stream_websocket_all.py) | Complete WebSocket reference (20+ subscription types) |

> **L4 Order Book**: Shows individual orders with order IDs. Essential for market making, order flow analysis, and optimal execution. Available via gRPC only. See [stream_l4_book.py](python/stream_l4_book.py) for details.

### Utilities
| Example | Description |
|---------|-------------|
| [markets.py](python/markets.py) | List all markets and DEXes |
| [open_orders.py](python/open_orders.py) | View open orders |
| [preflight.py](python/preflight.py) | Validate orders before signing |
| [approve.py](python/approve.py) | Manage builder fee approval |

### Complete Demo
| Example | Description |
|---------|-------------|
| [full_demo.py](python/full_demo.py) | All features in one file |

## Links

- **SDK Repository**: https://github.com/quiknode-labs/hyperliquid-sdk
- **SDK on PyPI**: https://pypi.org/project/hyperliquid-sdk/
- **Documentation**: https://hyperliquidapi.com/docs
- **QuickNode Docs**: https://www.quicknode.com/docs/hyperliquid

## Disclaimer

These are **unofficial community examples** developed and maintained by [QuickNode](https://quicknode.com). They are **not affiliated with, endorsed by, or associated with Hyperliquid Foundation or Hyperliquid Labs**.

Use at your own risk. Always review transactions before signing.

## License

MIT License
