import asyncio
from fastmcp import Client
from fastmcp.client.auth import OAuth



async def main():
    try:
        # Option 1: Simple OAuth (uses defaults) - RECOMMENDED
        # client = Client("http://localhost:8000/mcp", auth="oauth")

        # Option 2: Custom OAuth with specific scopes
        oauth = OAuth(
            mcp_url="http://localhost:8000/mcp",
            scopes=["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"]
        )

        # Connect to the FastMCP server with OAuth
        client = Client("http://localhost:8000/mcp", auth=oauth)

        async with client:
            print("🔐 OAuth authentication successful!\n")

            # List available tools
            tools = await client.list_tools()
            print("Available tools:\n")
            for tool in tools:
                print(tool)

            print("\n" + "="*50 + "\n")

            # Call the hello_world tool
            result = await client.call_tool("hello_world")
            print("Tool result:", result)

            print("\n" + "="*50 + "\n")

            # Call the get_weather tool
            result = await client.call_tool("get_weather", {"city": "New York"})
            print("Tool result:", result)
            print("Text Result:", result.content[0].text)
            print(result.content[0])

            await client.close()

    except Exception as e:
        print(f"❌ Error during OAuth connection: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
