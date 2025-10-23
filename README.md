# MCP Client/Server OAuth Project

A Python project demonstrating Model Context Protocol (MCP) client-server communication with Google OAuth authentication using the FastMCP framework.

## Project Structure

```
MCPClient_Server_Oauth/
├── MCPServer/          # MCP Server implementation with OAuth
│   ├── .venv/         # Server virtual environment
│   ├── .env           # OAuth credentials (not in git)
│   ├── pyproject.toml # Server dependencies
│   └── main.py        # Server entry point with GoogleProvider
│
├── MCPClient/          # MCP Client implementation
│   ├── .venv/         # Client virtual environment
│   ├── pyproject.toml # Client dependencies
│   └── main.py        # Client entry point with OAuth flow
│
└── Documentation/
    ├── CLAUDE.md              # Development guide
    ├── HOW_UV_WORKS.md        # UV detection algorithm explained
    ├── UV_GUIDE.md            # UV quick reference
    └── test_uv_detection.sh   # UV demonstration script
```

## Features

- **Google OAuth Authentication**: Secure authentication using Google OAuth 2.0
- **MCP Protocol**: Tool discovery and remote invocation via Model Context Protocol
- **FastMCP Framework**: Built on FastMCP 2.12.5+ for easy server/client development
- **Isolated Environments**: Separate virtual environments for server and client components

## Quick Start

### Prerequisites

- Python 3.12+
- UV package manager (`pip install uv` or see https://docs.astral.sh/uv/)
- Google Cloud Console OAuth credentials

### 1. Set Up Google OAuth

Before you can run the MCP Server successfully with Google OAuth Provider, follow these steps:

#### Create OAuth Credentials

1. **Create a Project in Google Cloud**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one

2. **Configure OAuth Consent Screen**
   - Navigate to **APIs & Services**
   - Click on **OAuth consent screen** in the left panel
   - Select **External** as the User Type (allows any Gmail account to be validated)
   - Fill in all required information:
     - App name
     - User support email
     - Developer contact information
   - Click **Save and Continue**
   - Add scopes if needed (optional for basic setup)
   - Add test users if desired (optional)
   - Complete the consent screen setup

3. **Create OAuth 2.0 Client ID**
   - Go back to **APIs & Services**
   - Click on **Credentials** in the left panel
   - Click **Create Credentials** → **OAuth 2.0 Client ID**
   - Select **Web application** as the application type
   - Choose a name for your OAuth client

4. **Configure Authorized Origins and Redirect URIs**
   - Under **Authorized JavaScript origins**, add:
     ```
     http://localhost:8000
     http://127.0.0.1:8000
     ```
   - Under **Authorized redirect URIs**, add:
     ```
     http://localhost:8000/auth/callback
     http://127.0.0.1:8000/auth/callback
     ```

5. **Save Credentials**
   - Click **Create**
   - Save your **Client ID** and **Client Secret** (you'll need these for the `.env` file)

#### Configure Server Environment

Create a `.env` file in the `MCPServer/` directory:

```bash
cd MCPServer
cat > .env << EOF
# Google OAuth client credentials (from Google Cloud Console)
GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-your-client-secret-here
EOF
```

**Important**: Replace `your-client-id-here` and `your-client-secret-here` with your actual credentials from Google Cloud Console.

### 2. Install Dependencies

```bash
# Install server dependencies
cd MCPServer
uv sync

# Install client dependencies
cd ../MCPClient
uv sync
```

### 3. Run the Server

```bash
cd MCPServer
uv run python main.py
```

You should see:
```
Starting MCP server on http://localhost:8000
MCP path: http://localhost:8000/mcp
Redirect path: http://localhost:8000/auth/callback
```

### 4. Run the Client

In a new terminal:

```bash
cd MCPClient
uv run python main.py
```

The OAuth flow will begin:
1. A browser window opens with Google login
2. Authenticate with your Google account
3. Grant permissions to the application
4. Browser redirects back to the server
5. Client successfully connects and lists available tools

Expected output:
```
🔐 OAuth authentication successful!

Available tools:
...

Tool result: Hello, world!
```

## Available Tools

The server exposes these MCP tools:

- **hello_world**: Returns a simple greeting message
- **get_weather**: Returns weather information for a specified city

Example usage from the client:

```python
# Call hello_world tool
result = await client.call_tool("hello_world")

# Call get_weather tool with parameters
result = await client.call_tool("get_weather", {"city": "New York"})
```

## Configuration

### Server Configuration (MCPServer/main.py)

The server can be configured via environment variables or the `.env` file:

```python
BASE_URL = "http://localhost:8000"              # Server base URL
REDIRECT_PATH = "/auth/callback"                # OAuth callback path
MCP_PATH = "/mcp"                               # MCP endpoint path
REQUIRED_SCOPES = [                             # Required OAuth scopes
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile"
]
ALLOWED_CLIENT_REDIRECT_URIS = [                # Client callback patterns
    "http://localhost:*",
    "http://127.0.0.1:*"
]
```

### Client Configuration (MCPClient/main.py)

The client connects to the server with OAuth:

```python
# Simple OAuth (recommended)
client = Client("http://localhost:8000/mcp", auth="oauth")

# Custom OAuth with specific scopes
oauth = OAuth(
    mcp_url="http://localhost:8000/mcp",
    scopes=["openid", "email", "profile"]
)
client = Client("http://localhost:8000/mcp", auth=oauth)
```

## Key Concepts

### OAuth Flow

1. **Client Initialization**: Client creates OAuth instance with MCP server URL
2. **Authorization Request**: Client redirects user to Google login
3. **User Authentication**: User logs in and grants permissions
4. **Callback Handling**: Google redirects to server's `/auth/callback`
5. **Token Exchange**: Server exchanges authorization code for access token
6. **Authenticated Connection**: Client uses token for MCP communication

### Virtual Environment Management

Each component has its own isolated virtual environment:

- **MCPServer/.venv**: Server dependencies (FastMCP, python-dotenv, Google auth)
- **MCPClient/.venv**: Client dependencies (FastMCP client libraries)

UV automatically detects which `.venv` to use based on your current directory. See [HOW_UV_WORKS.md](HOW_UV_WORKS.md) for details.

### MCP Protocol

The Model Context Protocol enables:
- **Tool Discovery**: List available tools and their schemas
- **Remote Invocation**: Call tools with typed parameters
- **Structured Responses**: Receive formatted results
- **Authentication**: Secure access via OAuth 2.0

## Documentation

- **[CLAUDE.md](CLAUDE.md)**: Complete development guide for working with this codebase
- **[HOW_UV_WORKS.md](HOW_UV_WORKS.md)**: Detailed explanation of UV's venv detection
- **[UV_GUIDE.md](UV_GUIDE.md)**: Quick reference for UV commands

## Common Commands

```bash
# Server
cd MCPServer
uv sync                    # Install/update dependencies
uv run python main.py      # Run server with OAuth

# Client
cd MCPClient
uv sync                    # Install/update dependencies
uv run python main.py      # Run client (triggers OAuth flow)

# Health check
curl http://localhost:8000/healthz

# Test UV detection
./test_uv_detection.sh
```

## Troubleshooting

### "ERR_UNSAFE_REDIRECT" in Browser

**Cause**: OAuth redirect URI not authorized in Google Cloud Console

**Solution**:
1. Go to Google Cloud Console → Credentials
2. Edit your OAuth 2.0 Client ID
3. Add `http://localhost:8000/auth/callback` to Authorized redirect URIs
4. Wait 5-10 minutes for changes to propagate

### "GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET is not set"

**Cause**: Missing or incorrect `.env` file in MCPServer/

**Solution**:
1. Create `.env` file in `MCPServer/` directory
2. Add your Google OAuth credentials (see [Set Up Google OAuth](#1-set-up-google-oauth))
3. Verify no duplicate prefixes in client secret (should be `GOCSPX-...`, not `GOCSPX-GOCSPX-...`)

### Client Connection Fails

**Cause**: Server not running or wrong URL

**Solution**:
1. Ensure server is running on `http://localhost:8000`
2. Check server logs for errors
3. Verify client is connecting to correct MCP endpoint (`http://localhost:8000/mcp`)

## Security Notes

- **Never commit `.env` files**: OAuth credentials should remain private
- **Use HTTPS in production**: OAuth should use secure connections
- **Rotate credentials**: Regularly update OAuth client secrets
- **Limit scopes**: Only request necessary OAuth scopes

## Dependencies

### Server (MCPServer/pyproject.toml)
- **FastMCP** (≥2.12.5): MCP server framework with OAuth support
- **python-dotenv**: Environment variable management
- **Google Auth**: OAuth provider integration

### Client (MCPClient/pyproject.toml)
- **FastMCP** (≥2.12.5): MCP client libraries with OAuth flow

Dependencies are managed via `pyproject.toml` and `uv.lock` files.

## Development

See [CLAUDE.md](CLAUDE.md) for:
- Architecture details
- Development workflows
- Testing procedures
- Best practices

## License

[Add your license here]
