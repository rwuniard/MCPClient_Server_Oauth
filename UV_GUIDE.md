# UV Virtual Environment Guide

## How UV Automatically Finds `.venv`

UV automatically detects and uses the `.venv` folder in your current directory or project root. **No configuration needed!**

## Project Structure

```
MCPClient_Server_Oauth/
├── MCPServer/
│   ├── .venv/          # Server's isolated environment
│   ├── pyproject.toml
│   └── main.py
└── MCPClient/
    ├── .venv/          # Client's isolated environment
    ├── pyproject.toml
    └── main.py
```

## Quick Commands

### Running Python with UV (Recommended)

```bash
# Server
cd MCPServer
uv run python main.py  # Auto-detects MCPServer/.venv

# Client
cd MCPClient
uv run python main.py  # Auto-detects MCPClient/.venv
```

### Installing Dependencies

```bash
# Sync dependencies from pyproject.toml
cd MCPServer
uv sync

# Add a new package
uv add requests

# Remove a package
uv remove requests
```

### Managing Virtual Environments

```bash
# Create a new .venv (if needed)
uv venv

# Create with specific Python version
uv venv --python 3.12

# Remove and recreate
rm -rf .venv
uv venv
uv sync
```

### Checking Active Environment

```bash
# Quick check
uv run python -c "import sys; print(sys.prefix)"

# Or use the check script
uv run python check_venv.py
```

## Manual Activation (Alternative)

If you prefer traditional activation:

```bash
# Linux/macOS
cd MCPServer
source .venv/bin/activate

# Windows
cd MCPServer
.venv\Scripts\activate
```

## Benefits of `uv run`

1. **No manual activation** - UV handles it automatically
2. **Correct environment always** - Based on current directory
3. **Consistent across systems** - Works the same everywhere
4. **No activation conflicts** - Each command uses the right env

## Common Issues

### Wrong environment being used?
```bash
# Check your current directory
pwd

# Make sure you're in the right component folder
cd MCPServer  # or MCPClient
```

### Dependencies not found?
```bash
# Install dependencies
cd MCPServer  # or MCPClient
uv sync
```

### Want to see installed packages?
```bash
cd MCPServer
uv pip list
```
