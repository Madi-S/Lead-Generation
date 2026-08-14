"""MCP (Model Context Protocol) server for py-lead-generation.

This module provides an MCP server that exposes lead generation
tools for use by AI assistants and automation workflows.

Tools:
    search_leads: Search for business leads using Google Maps or Yelp
    export_leads: Export collected leads to a CSV file
"""

from py_lead_generation.src.mcp.server import create_server, main

__all__ = ["main", "create_server"]
