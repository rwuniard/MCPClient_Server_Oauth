# How UV Understands Which `.venv` to Use

## UV's Virtual Environment Detection Algorithm

UV uses a **hierarchical search algorithm** that looks for virtual environments in a specific order based on your current working directory.

## The Search Algorithm (Step by Step)

```
┌─────────────────────────────────────┐
│ You run: uv run python main.py     │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ Step 1: Check Current Directory    │
│ Look for: ./.venv/                 │
└────────────┬────────────────────────┘
             │
             ├─ Found? ──► Use it! ✓
             │
             ▼ Not found?
┌─────────────────────────────────────┐
│ Step 2: Find Project Root          │
│ Search upward for: pyproject.toml  │
└────────────┬────────────────────────┘
             │
             ├─ Found? ──► Check for .venv in that directory
             │
             ▼ Not found?
┌─────────────────────────────────────┐
│ Step 3: Check Environment Variables│
│ Look for: $VIRTUAL_ENV             │
└────────────┬────────────────────────┘
             │
             ├─ Set? ──► Use it ✓
             │
             ▼ Not set?
┌─────────────────────────────────────┐
│ Step 4: Fall Back to System Python │
│ Use global Python installation     │
└─────────────────────────────────────┘
```

## Your Project Structure

```
MCPClient_Server_Oauth/          (no pyproject.toml here!)
├── MCPServer/
│   ├── pyproject.toml           ← Project boundary marker
│   ├── .venv/                   ← Virtual environment
│   │   ├── bin/
│   │   └── lib/
│   └── main.py
│
└── MCPClient/
    ├── pyproject.toml           ← Project boundary marker
    ├── .venv/                   ← Virtual environment
    │   ├── bin/
    │   └── lib/
    └── main.py
```

## How Detection Works in Your Setup

### Scenario 1: Running from MCPServer/

```bash
cd /path/to/MCPClient_Server_Oauth/MCPServer
uv run python main.py
```

**Detection Process:**
1. ✓ Check `./venv/` → **FOUND!** (/MCPServer/.venv)
2. ✓ Use MCPServer/.venv
3. ✓ Run python from MCPServer/.venv/bin/python

### Scenario 2: Running from MCPClient/

```bash
cd /path/to/MCPClient_Server_Oauth/MCPClient
uv run python main.py
```

**Detection Process:**
1. ✓ Check `./.venv/` → **FOUND!** (/MCPClient/.venv)
2. ✓ Use MCPClient/.venv
3. ✓ Run python from MCPClient/.venv/bin/python

### Scenario 3: Running from Root Directory

```bash
cd /path/to/MCPClient_Server_Oauth
uv run python MCPServer/main.py
```

**Detection Process:**
1. ✗ Check `./.venv/` → Not found
2. ✗ Search upward for `pyproject.toml` → Not found (root has none!)
3. ✗ Check environment variables → Not set
4. ✓ Fall back to **system Python** (not what you want!)

**⚠️ This is why you should always `cd` into the component directory first!**

## The Role of `pyproject.toml`

The `pyproject.toml` file serves **two critical purposes**:

1. **Project Boundary Marker**: Tells UV "stop searching here, this is the project root"
2. **Dependency Definition**: Defines what packages should be installed

### Example Flow

```
You are here: /MCPClient_Server_Oauth/MCPServer/src/utils/
Command: uv run python script.py

Search Process:
1. Check: /MCPClient_Server_Oauth/MCPServer/src/utils/.venv/ → Not found
2. Look up: /MCPClient_Server_Oauth/MCPServer/src/pyproject.toml → Not found
3. Look up: /MCPClient_Server_Oauth/MCPServer/pyproject.toml → FOUND! ✓
4. Check: /MCPClient_Server_Oauth/MCPServer/.venv/ → FOUND! ✓
5. Use: /MCPClient_Server_Oauth/MCPServer/.venv/
```

## Key Insights

### ✅ Why Your Setup Works

Each component has its own:
- `pyproject.toml` → Defines project boundary
- `.venv/` → Contains isolated dependencies

When you `cd` into a component, UV finds **both** files and uses that component's virtual environment.

### ❌ Common Mistakes

**Mistake 1: Running from wrong directory**
```bash
# BAD - uses wrong or no venv
cd /MCPClient_Server_Oauth
uv run python MCPServer/main.py

# GOOD - uses MCPServer/.venv
cd /MCPClient_Server_Oauth/MCPServer
uv run python main.py
```

**Mistake 2: Missing pyproject.toml**
```
MCPServer/
├── .venv/           ← venv exists
└── main.py          ← no pyproject.toml!
```
Without `pyproject.toml`, UV keeps searching upward and might find the wrong venv or use system Python.

**Mistake 3: Shared pyproject.toml**
```
MCPClient_Server_Oauth/
├── pyproject.toml   ← shared (BAD!)
├── .venv/           ← shared (BAD!)
├── MCPServer/
└── MCPClient/
```
Both components would share dependencies, defeating the purpose of isolation.

## Environment Variables (Advanced)

You can override UV's detection with environment variables:

```bash
# Force a specific venv
export VIRTUAL_ENV=/path/to/custom/.venv
uv run python main.py

# Or use UV's own variable
export UV_PROJECT_ENVIRONMENT=/path/to/.venv
uv run python main.py
```

## Verification Commands

```bash
# See which venv UV would use
cd MCPServer
uv run python -c "import sys; print(sys.prefix)"
# Output: /path/to/MCPServer/.venv

cd ../MCPClient
uv run python -c "import sys; print(sys.prefix)"
# Output: /path/to/MCPClient/.venv

# Check if venv is active
uv run python -c "import sys; print(sys.prefix != sys.base_prefix)"
# Output: True (venv is active)
```

## Best Practices

1. **Always have pyproject.toml** in each isolated component
2. **Always `cd` into the component** before running commands
3. **Use `uv run`** instead of manual activation for consistency
4. **Keep `.venv` in the same directory** as `pyproject.toml`
5. **One `pyproject.toml` per isolated environment**

## Summary

UV finds the correct `.venv` by:

1. **Looking in the current directory first** (./.venv)
2. **Searching upward for pyproject.toml** to find the project root
3. **Using the .venv in the project root** directory
4. **Stopping at the first pyproject.toml** it finds (project boundary)

The combination of `pyproject.toml` (boundary) + `.venv` (environment) in each component directory ensures UV always finds the right virtual environment based on where you run commands from.
