from fastmcp import FastMCP
from dotenv import load_dotenv
from fastmcp.server.auth.providers.google import GoogleProvider

from starlette.requests import Request          # (6) For our health check route signature
from starlette.responses import JSONResponse  

import os
import dotenv
import logging
import sys

# Configure root logger to output to console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

load_dotenv()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
logger.info(f"GOOGLE_CLIENT_ID: {GOOGLE_CLIENT_ID}")
logger.info(f"GOOGLE_CLIENT_SECRET: {GOOGLE_CLIENT_SECRET}")

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
REDIRECT_PATH = os.getenv("REDIRECT_PATH", "/auth/callback")
REQUIRED_SCOPES = os.getenv("REQUIRED_SCOPES", ["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"])
# Allow client callback servers on ANY localhost port (client uses random ports)
ALLOWED_CLIENT_REDIRECT_URIS = os.getenv("ALLOWED_CLIENT_REDIRECT_URIS", ["http://localhost:*", "http://127.0.0.1:*"])
MCP_PATH = os.getenv("MCP_PATH", "/mcp")

# Google authentication provider
google_auth = GoogleProvider(
    client_id = GOOGLE_CLIENT_ID,
    client_secret = GOOGLE_CLIENT_SECRET,
    base_url = BASE_URL,
    redirect_path = REDIRECT_PATH,
    required_scopes = REQUIRED_SCOPES,
    allowed_client_redirect_uris = ALLOWED_CLIENT_REDIRECT_URIS,
)

# Create a FastMCP with Oauth authentication
mcp = FastMCP("my-mcp-server", instructions=("MCP server that has hello_world and get_weather tools"), auth= google_auth)

# Create a FastMCP without Oauth authentication 
# mcp = FastMCP("my-mcp-server")



@mcp.tool()
def hello_world():
    return "Hello, world!"

@mcp.tool()
def get_weather(city: str):
    return f"The weather in {city} is sunny."

@mcp.custom_route("/healthz", methods=["GET"])
async def healthz(request: Request) -> JSONResponse:
    return JSONResponse(
        {
            "status": "ok",
            "base_url": BASE_URL,
            "mcp_path": "/mcp",
        }
    )

if __name__ == "__main__":
    if (GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None):
        logger.error("GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET is not set")
        exit(1)
    logger.info(f"Starting MCP server on {BASE_URL}")
    logger.info(f"MCP path: {BASE_URL}{MCP_PATH}")
    logger.info(f"Redirect path: {BASE_URL}/auth/callback")
    logger.info(f"Allowed client redirect URIs: {ALLOWED_CLIENT_REDIRECT_URIS}")
    logger.info(f"Google base URL: {BASE_URL}")
    logger.info(f"Google redirect path: {REDIRECT_PATH}")

    # Use "http" transport (recommended for OAuth flows)
    # Note: All FastMCP OAuth examples use "http", not "streamable-http"
    mcp.run(transport="http", host="0.0.0.0", port=8000, path=MCP_PATH)
    logger.info(f"Starting MCP server on {BASE_URL}{MCP_PATH}")