# Python Examples

Examples using the [Hyperliquid SDK](https://pypi.org/project/hyperliquid-sdk/) for Python.

## Installation

```bash
pip install hyperliquid-sdk
```

## Quick Start

```bash
# Set your private key
export PRIVATE_KEY="0x..."

# Run any example
python market_order.py
```

## Examples

### Order Placement
| File | Description |
|------|-------------|
| [market_order.py](market_order.py) | Market buy/sell that executes immediately |
| [place_order.py](place_order.py) | Limit order that rests on the book |
| [fluent_builder.py](fluent_builder.py) | Power user fluent API for orders |
| [hip3_order.py](hip3_order.py) | Trade HIP-3 markets (community perps) |

### Order Management
| File | Description |
|------|-------------|
| [cancel_order.py](cancel_order.py) | Cancel an order by OID |
| [cancel_by_cloid.py](cancel_by_cloid.py) | Cancel by client order ID |
| [cancel_all.py](cancel_all.py) | Cancel all open orders |
| [schedule_cancel.py](schedule_cancel.py) | Dead-man's switch auto-cancel |
| [modify_order.py](modify_order.py) | Modify a resting order |

### Position Management
| File | Description |
|------|-------------|
| [close_position.py](close_position.py) | Close a position completely |
| [roundtrip.py](roundtrip.py) | Buy then sell (complete cycle) |

### Market Data & Status
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
- **SDK Documentation**: https://hyperliquidapi.com/docs
