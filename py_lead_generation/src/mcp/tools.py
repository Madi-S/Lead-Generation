"""MCP tool definitions for lead generation.

This module defines the tools exposed by the MCP server:
- search_leads: Search for business leads
- export_leads: Export collected leads to CSV
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from mcp.types import TextContent, Tool

if TYPE_CHECKING:
    from py_lead_generation.src.google_maps.engine import GoogleMapsEngine
    from py_lead_generation.src.yelp.engine import YelpEngine

# Tool schemas for MCP
SEARCH_LEADS_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "description": "Search query (e.g., 'restaurants', 'gym', 'plumber')",
        },
        "location": {
            "type": "string",
            "description": "Location to search in (e.g., 'Paris', 'New York')",
        },
        "source": {
            "type": "string",
            "enum": ["google_maps", "yelp"],
            "default": "google_maps",
            "description": "Lead source to search",
        },
        "max_results": {
            "type": "integer",
            "default": 20,
            "description": "Maximum number of results to return",
        },
    },
    "required": ["query", "location"],
}

EXPORT_LEADS_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "filename": {
            "type": "string",
            "default": "leads.csv",
            "description": "Output filename for the CSV export",
        },
        "format": {
            "type": "string",
            "enum": ["csv"],
            "default": "csv",
            "description": "Export format (currently only CSV supported)",
        },
    },
}

LIST_SOURCES_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {},
}


def get_tools() -> list[Tool]:
    """Get list of available MCP tools.

    Returns:
        List of Tool definitions for MCP server
    """
    return [
        Tool(
            name="search_leads",
            description=(
                "Search for business leads using Google Maps or Yelp. "
                "Returns a list of businesses with contact information."
            ),
            inputSchema=SEARCH_LEADS_SCHEMA,
        ),
        Tool(
            name="export_leads",
            description=(
                "Export collected leads to a CSV file. "
                "Must be called after search_leads to have data to export."
            ),
            inputSchema=EXPORT_LEADS_SCHEMA,
        ),
        Tool(
            name="list_sources",
            description="List available lead generation sources.",
            inputSchema=LIST_SOURCES_SCHEMA,
        ),
    ]


# In-memory storage for collected leads (per session)
_collected_leads: list[dict[str, str]] = []


async def handle_search_leads(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle search_leads tool call.

    Args:
        arguments: Tool arguments from MCP client

    Returns:
        List of TextContent with search results
    """
    query = arguments.get("query", "")
    location = arguments.get("location", "")
    source = arguments.get("source", "google_maps")

    if not query or not location:
        return [TextContent(type="text", text="Error: query and location are required")]

    try:
        if source == "google_maps":
            from py_lead_generation.src.google_maps.engine import GoogleMapsEngine
            engine: GoogleMapsEngine | YelpEngine = GoogleMapsEngine(query, location)
        elif source == "yelp":
            from py_lead_generation.src.yelp.engine import YelpEngine
            engine = YelpEngine(query, location)
        else:
            return [TextContent(type="text", text=f"Error: Unknown source '{source}'")]

        await engine.run()
        leads = engine.entries

        # Store for later export
        global _collected_leads
        _collected_leads.extend(leads)

        # Format results
        result_text = f"Found {len(leads)} leads for '{query}' in '{location}':\n\n"
        for i, lead in enumerate(leads[:10], 1):  # Show first 10
            result_text += f"{i}. {lead.get('Title', 'N/A')}\n"
            result_text += f"   Address: {lead.get('Address', 'N/A')}\n"
            result_text += f"   Phone: {lead.get('PhoneNumber', 'N/A')}\n\n"

        if len(leads) > 10:
            result_text += f"... and {len(leads) - 10} more results.\n"

        return [TextContent(type="text", text=result_text)]

    except Exception as e:
        return [TextContent(type="text", text=f"Error searching leads: {e}")]


async def handle_export_leads(arguments: dict[str, Any]) -> list[TextContent]:
    """Handle export_leads tool call.

    Args:
        arguments: Tool arguments from MCP client

    Returns:
        List of TextContent with export status
    """
    filename = arguments.get("filename", "leads.csv")

    if not _collected_leads:
        return [TextContent(
            type="text",
            text="No leads to export. Run search_leads first."
        )]

    try:
        from py_lead_generation.src.misc.writer import CsvWriter

        # Determine field names from first lead
        field_names = list(_collected_leads[0].keys())
        writer = CsvWriter(filename, field_names)
        writer.append(_collected_leads)

        return [TextContent(
            type="text",
            text=f"Exported {len(_collected_leads)} leads to {filename}"
        )]

    except Exception as e:
        return [TextContent(type="text", text=f"Error exporting leads: {e}")]


async def handle_list_sources(_arguments: dict[str, Any]) -> list[TextContent]:
    """Handle list_sources tool call.

    Returns:
        List of TextContent with available sources
    """
    sources = [
        "google_maps - Google Maps business listings",
        "yelp - Yelp business directory",
        "twogis - 2GIS (coming soon)",
    ]
    return [TextContent(type="text", text="Available sources:\n" + "\n".join(sources))]


async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Route tool calls to appropriate handlers.

    Args:
        name: Tool name to call
        arguments: Tool arguments

    Returns:
        List of TextContent with tool results
    """
    handlers = {
        "search_leads": handle_search_leads,
        "export_leads": handle_export_leads,
        "list_sources": handle_list_sources,
    }

    handler = handlers.get(name)
    if handler:
        return await handler(arguments)

    return [TextContent(type="text", text=f"Unknown tool: {name}")]
