from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()


mcp = FastMCP("my-mcp-server", )


@mcp.tool()
def hello_world():
    return "Hello, world!"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
