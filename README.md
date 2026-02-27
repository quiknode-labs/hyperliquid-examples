# Hyperliquid Examples

> **Community Examples by [QuickNode](https://quicknode.com)** — Not affiliated with Hyperliquid Foundation.

Runnable examples using the [Hyperliquid SDK](https://github.com/quiknode-labs/hyperliquid-sdk) for trading on Hyperliquid.

## Available Examples

| Language | Directory | Status |
|----------|-----------|--------|
| [Python](./python/) | `cd python && python market_order.py` | Available |
| [TypeScript](./typescript/) | `cd typescript && npx ts-node market_order.ts` | Coming soon |
| [Rust](./rust/) | `cd rust && cargo run --example market_order` | Coming soon |

## Quick Start

### Python

```bash
# Install the SDK
pip install hyperliquid-sdk

# Set credentials
export PRIVATE_KEY="0x..."
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

## Example Categories

Each language directory contains examples for:

- **Trading** — Market orders, limit orders, order management
- **Info API** — Market data, user positions, order book
- **HyperCore API** — Block data, recent trades
- **HyperEVM** — Ethereum JSON-RPC calls
- **Streaming** — WebSocket and gRPC real-time data (L2/L4 order book)

See the README in each language directory for the full list.

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
