# MCP Client/Server OAuth Project

A Python project demonstrating Model Context Protocol (MCP) client-server communication using FastMCP framework.

## Project Structure

```
MCPClient_Server_Oauth/
├── MCPServer/          # MCP Server implementation
│   ├── .venv/         # Server virtual environment
│   ├── pyproject.toml # Server dependencies
│   └── main.py        # Server entry point
│
├── MCPClient/          # MCP Client implementation
│   ├── .venv/         # Client virtual environment
│   ├── pyproject.toml # Client dependencies
│   └── main.py        # Client entry point
│
└── Documentation/
    ├── CLAUDE.md              # Development guide
    ├── HOW_UV_WORKS.md        # UV detection algorithm explained
    ├── UV_GUIDE.md            # UV quick reference
    └── test_uv_detection.sh   # UV demonstration script
```

## Quick Start

### Prerequisites

- Python 3.12+
- UV package manager (`pip install uv` or see https://docs.astral.sh/uv/)

### Running the Server

```bash
cd MCPServer
uv run python main.py
```

The server will start on `http://localhost:8000`

### Running the Client

```bash
cd MCPClient
uv run python main.py
```

The client connects to the server and invokes available tools.

## Key Concepts

### Virtual Environment Management

Each component (server/client) has its own isolated virtual environment:

- **MCPServer/.venv** - Server dependencies (FastMCP, server libraries)
- **MCPClient/.venv** - Client dependencies (FastMCP client libraries)

UV automatically detects which `.venv` to use based on your current directory. See [HOW_UV_WORKS.md](HOW_UV_WORKS.md) for details.

### MCP Protocol

The Model Context Protocol enables:
- Tool discovery and registration
- Remote tool invocation
- Structured request/response handling

## Documentation

- **[CLAUDE.md](CLAUDE.md)** - Complete development guide for working with this codebase
- **[HOW_UV_WORKS.md](HOW_UV_WORKS.md)** - Detailed explanation of UV's venv detection
- **[UV_GUIDE.md](UV_GUIDE.md)** - Quick reference for UV commands

## Common Commands

```bash
# Server
cd MCPServer
uv sync              # Install dependencies
uv run python main.py  # Run server

# Client
cd MCPClient
uv sync              # Install dependencies
uv run python main.py  # Run client

# Test UV detection
./test_uv_detection.sh
```

## Dependencies

Both components use:
- **FastMCP** (≥2.12.5) - Framework for building MCP servers and clients
- **Python** (≥3.12) - Runtime environment

Dependencies are managed via `pyproject.toml` and `uv.lock` files.

## Development

See [CLAUDE.md](CLAUDE.md) for:
- Architecture details
- Development workflows
- Testing procedures
- Best practices

## License

[Add your license here]
