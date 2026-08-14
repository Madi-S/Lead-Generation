"""MCP server for lead generation.

This module provides the main MCP server implementation that exposes
lead generation tools for use by AI assistants and automation workflows.

Usage:
    # As a module
    from py_lead_generation.src.mcp import create_server
    server = create_server()

    # From command line
    lead-gen-mcp
"""

from __future__ import annotations

import asyncio
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from py_lead_generation.src.mcp.tools import call_tool, get_tools


def create_server() -> Server:
    """Create and configure the MCP server.

    Returns:
        Configured MCP Server instance
    """
    server = Server("lead-generation")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available lead generation tools."""
        return get_tools()

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict[str, Any] | None
    ) -> list[TextContent]:
        """Handle tool calls from MCP clients."""
        return await call_tool(name, arguments or {})

    return server


async def run_server() -> None:
    """Run the MCP server using stdio transport."""
    server = create_server()

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def main() -> None:
    """Entry point for lead-gen-mcp command."""
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
