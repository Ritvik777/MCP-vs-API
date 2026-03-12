"""
MCP CLIENT — Connects to the server and calls a tool.

This discovers what tools the server has, then calls one.
The same code works with ANY MCP server — weather, GitHub,
database, anything. That's the whole point of MCP.
"""

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = Path(__file__).parent / "server.py"


async def main():
    # Connect to our server (runs server.py as a subprocess)
    async with stdio_client(
        StdioServerParameters(command=sys.executable, args=[str(SERVER)])
    ) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Ask the server: "What tools do you have?"
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"Found tool: {tool.name}")

            # Call the tool
            print("\nGetting forecast for San Francisco...\n")
            result = await session.call_tool(
                "get_forecast",
                arguments={"latitude": 37.7749, "longitude": -122.4194},
            )
            print(result.content[0].text)


asyncio.run(main())
