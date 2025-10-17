# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **MCP (Model Context Protocol) Client/Server OAuth** project with two main components:
- **MCPServer/**: A FastMCP-based server implementation providing MCP tools
- **MCPClient/**: Client implementation (currently empty/in development)

The server uses FastMCP 2.12.5+ framework to expose tools via the Model Context Protocol.

## Architecture

### MCPServer Structure

The server is built on FastMCP (https://github.com/jlowin/fastmcp), a lightweight framework for creating MCP servers.

**Key architectural notes:**
- **main.py**: Contains tool definitions using `@mcp.tool()` decorator
- **FastMCP instance**: Created with `mcp = FastMCP("my-mcp-server")` and must be instantiated BEFORE decorator usage
- **Tool registration**: Tools are defined via decorators but must be registered before FastMCP instantiation

**Current bug in main.py**: The decorator `@mcp.tool()` is used before `mcp` is defined. The correct pattern is:
```python
mcp = FastMCP("my-mcp-server")

@mcp.tool()
def hello_world():
    return "Hello, world!"
```

## Development Commands

### Environment Setup

**UV automatically detects `.venv` in each component directory!** No manual configuration needed.

```bash
# Option 1: Use uv run (recommended - automatic venv detection)
cd MCPServer
uv run python main.py

# Option 2: Manual activation
cd MCPServer
source .venv/bin/activate
python main.py

# Install/sync dependencies (uv auto-uses local .venv)
cd MCPServer
uv sync
```

**How UV finds .venv:**
- UV searches for `.venv` in the current directory
- If not found, searches upward for `pyproject.toml` (project boundary marker)
- Each component (MCPServer, MCPClient) has its own isolated `.venv` + `pyproject.toml`
- Simply `cd` into the component directory and UV uses the right environment
- **See [HOW_UV_WORKS.md](HOW_UV_WORKS.md) for detailed explanation of the detection algorithm**

### Running the MCP Server
```bash
# Recommended: Use uv run
cd MCPServer
uv run python main.py

# Alternative: Manual activation
cd MCPServer
source .venv/bin/activate
python main.py
```

### Testing Tools
```bash
# Run the FastMCP CLI to test tools
fastmcp dev main.py
```

### Running the MCP Client
```bash
# Recommended: Use uv run
cd MCPClient
uv run python main.py

# Alternative: Manual activation
cd MCPClient
source .venv/bin/activate
python main.py
```

**Important**: The server must be running on `http://localhost:8000` before starting the client.

## Python Environment

- **Python version**: 3.12+ (tested with 3.12.8)
- **Package manager**: uv (modern Python package manager)
- **Virtual environments**:
  - `MCPServer/.venv/` - Server dependencies
  - `MCPClient/.venv/` - Client dependencies
  - UV automatically detects and uses the correct `.venv` based on current directory
- **Dependencies**: Managed via `pyproject.toml` and `uv.lock` in each component

## MCP Protocol Integration

This server implements the Model Context Protocol, which allows AI models to:
1. Discover available tools via MCP protocol
2. Invoke tools with parameters
3. Receive structured responses

Tools are exposed through the FastMCP framework's built-in MCP server implementation.

### MCPClient Structure

The client connects to the FastMCP server to invoke tools remotely.

**Key patterns:**
- **Async/await required**: All client operations are asynchronous and require `asyncio.run()`
- **Client initialization**: `Client("http://localhost:8000/mcp")` - uses simple URL string
- **Context manager**: Always use `async with client:` for proper connection handling
- **Available operations**: `list_tools()`, `call_tool(name, args)`, `list_resources()`, `ping()`

## Development Notes

- The server uses FastMCP's automatic protocol handling
- Tool definitions should be simple Python functions with type hints for automatic schema generation
- Client and server communicate over HTTP using the MCP protocol
