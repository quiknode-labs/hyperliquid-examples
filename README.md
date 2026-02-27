# Hyperliquid Examples

> **Community Examples by [QuickNode](https://quicknode.com)** — Not affiliated with Hyperliquid Foundation.

Examples using the [Hyperliquid SDK](https://github.com/quiknode-labs/hyperliquid-sdk) for trading on Hyperliquid.

## Quick Start

### Python

```bash
# Install the SDK
pip install hyperliquid-sdk

# Set your private key
export PRIVATE_KEY="0x..."

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

### Order Placement
| Example | Description |
|---------|-------------|
| [market_order.py](python/market_order.py) | Market buy/sell that executes immediately |
| [place_order.py](python/place_order.py) | Limit order that rests on the book |
| [fluent_builder.py](python/fluent_builder.py) | Power user fluent API for orders |
| [hip3_order.py](python/hip3_order.py) | Trade HIP-3 markets (community perps) |

### Order Management
| Example | Description |
|---------|-------------|
| [cancel_order.py](python/cancel_order.py) | Cancel an order by OID |
| [cancel_by_cloid.py](python/cancel_by_cloid.py) | Cancel by client order ID |
| [cancel_all.py](python/cancel_all.py) | Cancel all open orders |
| [schedule_cancel.py](python/schedule_cancel.py) | Dead-man's switch auto-cancel |
| [modify_order.py](python/modify_order.py) | Modify a resting order |

### Position Management
| Example | Description |
|---------|-------------|
| [close_position.py](python/close_position.py) | Close a position completely |
| [roundtrip.py](python/roundtrip.py) | Buy then sell (complete cycle) |

### Market Data & Status
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

## Disclaimer

These are **unofficial community examples** developed and maintained by [QuickNode](https://quicknode.com). They are **not affiliated with, endorsed by, or associated with Hyperliquid Foundation or Hyperliquid Labs**.

Use at your own risk. Always review transactions before signing.

## License

MIT License
