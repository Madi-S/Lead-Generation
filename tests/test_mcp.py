"""Tests for MCP server and tools."""


def test_mcp_tools_import() -> None:
    """Test that MCP tools can be imported."""
    from py_lead_generation.src.mcp.tools import get_tools

    assert get_tools is not None


def test_mcp_server_import() -> None:
    """Test that MCP server can be imported."""
    from py_lead_generation.src.mcp.server import create_server

    assert create_server is not None


def test_mcp_tools_list() -> None:
    """Test that get_tools returns a list of tools."""
    from py_lead_generation.src.mcp.tools import get_tools

    tools = get_tools()
    assert isinstance(tools, list)
    assert len(tools) >= 2  # At least search_leads and export_leads


def test_mcp_tool_names() -> None:
    """Test that expected tools are present."""
    from py_lead_generation.src.mcp.tools import get_tools

    tools = get_tools()
    tool_names = [t.name for t in tools]

    assert "search_leads" in tool_names
    assert "export_leads" in tool_names


def test_mcp_server_creation() -> None:
    """Test that MCP server can be created."""
    from py_lead_generation.src.mcp.server import create_server

    server = create_server()
    assert server is not None
    assert server.name == "lead-generation"
