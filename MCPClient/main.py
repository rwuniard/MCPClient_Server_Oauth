import asyncio
from fastmcp import Client


async def main():
    # Connect to the FastMCP server
    # You can use a simple URL string instead of creating a transport manually
    client = Client("http://localhost:8000/mcp")

    async with client:
        # List available tools
        tools = await client.list_tools()
        print("Available tools:", tools)

        # Call the hello_world tool
        result = await client.call_tool("hello_world")
        print("Tool result:", result)


if __name__ == "__main__":
    asyncio.run(main())
