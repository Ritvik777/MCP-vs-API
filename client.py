"""
MCP Client Demo
===============
Connects to the weather MCP server, discovers tools automatically,
and calls get_forecast. Demonstrates how any MCP client can use
any MCP server through the standard protocol.

Run:
    uv run client.py
    # or
    python client.py
"""

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_SCRIPT = Path(__file__).parent / "server.py"


async def main():
    print("Connecting to weather MCP server...\n")

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_SCRIPT)],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # --- Discover available tools (no hardcoded knowledge needed) ---
            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")

            # --- Call get_forecast for San Francisco ---
            print("\nFetching forecast for San Francisco (37.77, -122.42)...\n")
            result = await session.call_tool(
                "get_forecast",
                arguments={"latitude": 37.7749, "longitude": -122.4194},
            )
            print(result.content[0].text)

            # --- Call get_alerts for California ---
            print("\n" + "=" * 50)
            print("Fetching weather alerts for California...\n")
            result = await session.call_tool(
                "get_alerts",
                arguments={"state": "CA"},
            )
            print(result.content[0].text)


if __name__ == "__main__":
    asyncio.run(main())
