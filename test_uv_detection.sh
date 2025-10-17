#!/bin/bash
# Script to demonstrate UV's .venv detection algorithm

echo "================================================"
echo "UV Virtual Environment Detection Demonstration"
echo "================================================"
echo ""

# Store the root directory
ROOT_DIR="/Users/ronsonw/Projects/python/MCPClient_Server_Oauth"

# Test 1: From MCPServer directory
echo "Test 1: Running from MCPServer directory"
echo "Command: cd MCPServer && uv run python -c '...'"
cd "$ROOT_DIR/MCPServer"
echo "Current directory: $(pwd)"
VENV=$(uv run python -c "import sys; print(sys.prefix)" 2>&1)
echo "Detected venv: $VENV"
echo ""

# Test 2: From MCPClient directory
echo "Test 2: Running from MCPClient directory"
echo "Command: cd MCPClient && uv run python -c '...'"
cd "$ROOT_DIR/MCPClient"
echo "Current directory: $(pwd)"
VENV=$(uv run python -c "import sys; print(sys.prefix)" 2>&1)
echo "Detected venv: $VENV"
echo ""

# Test 3: From root directory (no pyproject.toml)
echo "Test 3: Running from root directory (no pyproject.toml here)"
echo "Command: cd root && uv run python -c '...'"
cd "$ROOT_DIR"
echo "Current directory: $(pwd)"
VENV=$(uv run python -c "import sys; print(sys.prefix)" 2>&1)
echo "Detected venv: $VENV"
echo "⚠️  Notice: Uses system Python, not a project venv!"
echo ""

# Test 4: From nested directory within MCPServer
echo "Test 4: Running from nested directory (if it existed)"
echo "This would search upward until finding pyproject.toml"
echo "Then use the .venv in that directory"
echo ""

echo "================================================"
echo "Summary"
echo "================================================"
echo "✓ MCPServer directory → uses MCPServer/.venv"
echo "✓ MCPClient directory → uses MCPClient/.venv"
echo "✗ Root directory → uses system Python (no project)"
echo ""
echo "Key Insight: pyproject.toml marks project boundaries!"
echo "UV stops searching when it finds pyproject.toml"
echo ""
