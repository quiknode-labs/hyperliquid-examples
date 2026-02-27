# Python Examples

Examples using the [Hyperliquid SDK](https://pypi.org/project/hyperliquid-sdk/) for Python.

## Installation

```bash
pip install hyperliquid-sdk
```

## Quick Start

```bash
# Set your private key (for trading examples)
export PRIVATE_KEY="0x..."

# Set your endpoint (for data examples)
export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"

# Run any example
python market_order.py
```

## Examples

### Trading — Order Placement
| File | Description |
|------|-------------|
| [market_order.py](market_order.py) | Market buy/sell that executes immediately |
| [place_order.py](place_order.py) | Limit order that rests on the book |
| [fluent_builder.py](fluent_builder.py) | Power user fluent API for orders |
| [hip3_order.py](hip3_order.py) | Trade HIP-3 markets (community perps) |

### Trading — Order Management
| File | Description |
|------|-------------|
| [cancel_order.py](cancel_order.py) | Cancel an order by OID |
| [cancel_by_cloid.py](cancel_by_cloid.py) | Cancel by client order ID |
| [cancel_all.py](cancel_all.py) | Cancel all open orders |
| [schedule_cancel.py](schedule_cancel.py) | Dead-man's switch auto-cancel |
| [modify_order.py](modify_order.py) | Modify a resting order |

### Trading — Position Management
| File | Description |
|------|-------------|
| [close_position.py](close_position.py) | Close a position completely |
| [roundtrip.py](roundtrip.py) | Buy then sell (complete cycle) |

### Info API — Market Data
| File | Description |
|------|-------------|
| [info_market_data.py](info_market_data.py) | Mid prices, order book, recent trades |
| [info_user_data.py](info_user_data.py) | Account state, positions, orders |
| [info_candles.py](info_candles.py) | OHLCV candlestick data |
| [info_vaults.py](info_vaults.py) | Vault summaries and details |
| [info_batch_queries.py](info_batch_queries.py) | Batch queries for multiple users |

### HyperCore API — Block Data
| File | Description |
|------|-------------|
| [hypercore_blocks.py](hypercore_blocks.py) | Blocks, trades, and order events |

### HyperEVM — Ethereum JSON-RPC
| File | Description |
|------|-------------|
| [evm_basics.py](evm_basics.py) | Chain ID, blocks, balances |

### Real-Time Streaming
| File | Description |
|------|-------------|
| [stream_trades.py](stream_trades.py) | WebSocket streaming basics (trades, L2 book, all mids, BBO) |
| [stream_grpc.py](stream_grpc.py) | gRPC streaming basics (trades, L2/L4 book, blocks) |
| [stream_orderbook.py](stream_orderbook.py) | L2 and L4 order book comparison |
| [stream_l4_book.py](stream_l4_book.py) | **L4 order book (individual orders) — CRITICAL** |
| [stream_l2_book.py](stream_l2_book.py) | L2 order book (gRPC vs WebSocket) |
| [stream_websocket_all.py](stream_websocket_all.py) | Complete WebSocket reference (20+ subscription types) |

### Utilities
| File | Description |
|------|-------------|
| [markets.py](markets.py) | List all markets and DEXes |
| [open_orders.py](open_orders.py) | View open orders |
| [preflight.py](preflight.py) | Validate orders before signing |
| [approve.py](approve.py) | Manage builder fee approval |

### Complete Demo
| File | Description |
|------|-------------|
| [full_demo.py](full_demo.py) | All features in one file |

## Links

- **SDK on PyPI**: https://pypi.org/project/hyperliquid-sdk/
- **SDK Repository**: https://github.com/quiknode-labs/hyperliquid-sdk
- **SDK Documentation**: https://hyperliquidapi.com/docs
- **QuickNode Docs**: https://www.quicknode.com/docs/hyperliquid
