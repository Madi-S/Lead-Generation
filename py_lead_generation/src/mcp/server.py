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

from mcp.server import Server
from mcp.server.lowlevel.server import ServerRequestContext
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequestParams,
    CallToolResult,
    ListToolsResult,
    PaginatedRequestParams,
)

from py_lead_generation.src.mcp.tools import call_tool, get_tools


def create_server() -> Server:
    """Create and configure the MCP server.

    Returns:
        Configured MCP Server instance
    """
    async def list_tools(
        _context: ServerRequestContext, _params: PaginatedRequestParams | None
    ) -> ListToolsResult:
        """List available lead generation tools."""
        return ListToolsResult(tools=get_tools())

    async def handle_call_tool(
        _context: ServerRequestContext, params: CallToolRequestParams
    ) -> CallToolResult:
        """Handle tool calls from MCP clients."""
        content = await call_tool(params.name, params.arguments or {})
        return CallToolResult(content=content)

    server = Server(
        "lead-generation",
        on_list_tools=list_tools,
        on_call_tool=handle_call_tool,
    )

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
