# Hyperliquid Examples

> **Community Examples by [QuickNode](https://quicknode.com)** — Not affiliated with Hyperliquid Foundation.

Runnable examples using the [Hyperliquid SDK](https://github.com/quiknode-labs/hyperliquid-sdk) for trading on Hyperliquid.

## Available Examples

| Language | Package | Registry |
|----------|---------|----------|
| [Python](./python/) | `hyperliquid-sdk` | [PyPI](https://pypi.org/project/hyperliquid-sdk/) |
| [TypeScript](./typescript/) | `@quicknode/hyperliquid-sdk` | [npm](https://www.npmjs.com/package/@quicknode/hyperliquid-sdk) |
| [Rust](./rust/) | `quicknode-hyperliquid-sdk` | [crates.io](https://crates.io/crates/quicknode-hyperliquid-sdk) |
| [Go](./go/) | `github.com/quiknode-labs/hyperliquid-sdk/go` | [GitHub](https://github.com/quiknode-labs/hyperliquid-sdk) |

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

### TypeScript

```bash
cd typescript

# Install dependencies
npm install

# Set credentials
export PRIVATE_KEY="0x..."
export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"

# Run any example
npx tsx market_order.ts
```

### Rust

```bash
cd rust

# Set credentials
export PRIVATE_KEY="0x..."
export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"

# Run any example
cargo run --bin market_order
```

### Go

```bash
cd go

# Set credentials
export PRIVATE_KEY="0x..."
export ENDPOINT="https://your-endpoint.hype-mainnet.quiknode.pro/YOUR_TOKEN"

# Run any example
go run ./market_order
```

## Example Categories

Each language directory contains examples for:

- **Trading** — Market orders, limit orders, order management
- **Info API** — Market data, user positions, order book
- **HyperCore API** — Block data, recent trades
- **HyperEVM** — Ethereum JSON-RPC calls
- **Streaming** — WebSocket and gRPC real-time data (L2/L4 order book)

## Links

- **SDK Repository**: https://github.com/quiknode-labs/hyperliquid-sdk
- **SDK on PyPI**: https://pypi.org/project/hyperliquid-sdk/
- **SDK on npm**: https://www.npmjs.com/package/@quicknode/hyperliquid-sdk
- **SDK on crates.io**: https://crates.io/crates/quicknode-hyperliquid-sdk
- **Documentation**: https://hyperliquidapi.com
- **QuickNode Docs**: https://www.quicknode.com/docs/hyperliquid

## Disclaimer

These are **unofficial community examples** developed and maintained by [QuickNode](https://quicknode.com). They are **not affiliated with, endorsed by, or associated with Hyperliquid Foundation or Hyperliquid Labs**.

Use at your own risk. Always review transactions before signing.

## License

MIT License
