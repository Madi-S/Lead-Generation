# Implementation Plan: Package Setup, MCP Server & Mailing Integration

**Branch**: `001-package-setup-mcp` | **Date**: 2026-01-09 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-package-setup-mcp/spec.md`

## Summary

This plan covers five user stories: (P1) package cleanup and structure consolidation, (P2) MCP server with lead generation tools, (P3) Gmail SMTP email outreach, (P4) tkinter GUI, and (P5) 2GIS engine interface stub. Primary focus is on establishing a clean, maintainable package foundation with modern Python tooling while adding MCP and email integration.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**:
- Existing: `beautifulsoup4`, `geopy`, `playwright`, `python-slugify`
- New: `mcp` (Model Context Protocol SDK), `tkinter` (stdlib)
- Email: `smtplib`, `email` (stdlib - no new deps needed)
**Storage**: CSV files for lead export, `.env` or config files for credentials
**Testing**: pytest, pytest-playwright
**Target Platform**: Cross-platform (Linux, macOS, Windows)
**Project Type**: Single Python package
**Package Manager**: uv (with pyproject.toml, hatchling backend)
**Performance Goals**: MCP response <500ms, email send <10s per message
**Constraints**: Minimal dependencies, Python stdlib preferred where possible
**Scale/Scope**: Individual/small team usage, 100s-1000s of leads per session

## Constitution Check

*GATE: Must pass before implementation. Verified against py-lead-generation Constitution v1.0.0*

| Principle | Compliance | Notes |
|-----------|------------|-------|
| I. Engine Architecture | ✅ PASS | 2GIS engine will follow `AbstractEngine` → `BaseEngine` pattern |
| II. Async-First Design | ✅ PASS | MCP server and email sender will use async patterns |
| III. SOLID & Readable Code | ✅ PASS | Type hints, docstrings, <50 line functions required |
| IV. Extensibility | ✅ PASS | MCP tools are modular; email uses interface pattern |
| V. Data Export | ✅ PASS | Existing CSV export preserved; no changes needed |

## Project Structure

### Documentation (this feature)

```text
specs/001-package-setup-mcp/
├── plan.md              # This file
├── spec.md              # Feature specification
├── checklists/
│   └── requirements.md  # Specification validation checklist
└── tasks.md             # Task breakdown (created by /speckit.tasks)
```

### Source Code (repository root)

```text
py_lead_generation/
├── __init__.py              # Public API exports (GoogleMapsEngine, YelpEngine, TwoGisEngine)
├── src/
│   ├── __init__.py
│   ├── engines/
│   │   ├── __init__.py
│   │   ├── abstract.py      # AbstractEngine base class
│   │   ├── base.py          # BaseEngine implementation
│   │   └── playwright_config.py
│   ├── google_maps/
│   │   ├── __init__.py
│   │   └── engine.py        # GoogleMapsEngine
│   ├── yelp/
│   │   ├── __init__.py
│   │   └── engine.py        # YelpEngine
│   ├── twogis/              # NEW: 2GIS engine stub
│   │   ├── __init__.py
│   │   └── engine.py        # TwoGisEngine (interface only)
│   ├── mcp/                 # NEW: MCP server
│   │   ├── __init__.py
│   │   ├── server.py        # MCP server implementation
│   │   └── tools.py         # Tool definitions (search_leads, export_leads)
│   ├── email/               # NEW: Email outreach
│   │   ├── __init__.py
│   │   ├── sender.py        # GmailSMTPSender class
│   │   ├── templates.py     # EmailTemplate class
│   │   └── config.py        # SMTPConfig dataclass
│   ├── gui/                 # NEW: Tkinter GUI
│   │   ├── __init__.py
│   │   └── app.py           # Main GUI application
│   └── misc/
│       ├── __init__.py
│       ├── utils.py         # Geocoding utilities
│       └── writer.py        # CsvWriter

tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_sample.py           # Existing basic tests
├── test_engines.py          # NEW: Engine instantiation tests (mocked)
├── test_mcp.py              # NEW: MCP tool tests (mocked)
└── test_email.py            # NEW: Email sender tests (mocked)

# Root level
├── pyproject.toml           # Single source of truth for deps
├── .pre-commit-config.yaml  # Pre-commit hooks
├── .env.example             # NEW: Example environment variables
├── README.md                # Updated with new features
└── run.py                   # Example usage script

# REMOVED:
# - archived/                 # Legacy code (DELETE)
# - py_lead_generation/requirements.txt  # Duplicate deps (DELETE)
# - .github/workflows/python-publish.yml  # Duplicate workflow (DELETE)
# - setup.py                  # Legacy setuptools (DELETE)
```

## Research Notes

### MCP Server Implementation

The `mcp` Python SDK provides the standard way to create MCP servers:

```python
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("lead-generation")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(name="search_leads", description="...", inputSchema={...}),
        Tool(name="export_leads", description="...", inputSchema={...}),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    ...
```

**Dependency**: `mcp>=1.0.0` (add to pyproject.toml)

### Gmail SMTP Configuration

Gmail requires:
1. App Password (not regular password) for SMTP
2. 2FA enabled on account
3. SMTP settings: `smtp.gmail.com:587` with STARTTLS

Configuration via environment variables:
```
GMAIL_ADDRESS=user@gmail.com
GMAIL_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
```

### Tkinter GUI

Tkinter is included in Python stdlib. Basic structure:
- Main window with search form (query, location inputs)
- Results display (Treeview widget for tabular data)
- Export button
- Async integration via `asyncio` and `after()` callbacks

## Data Model

### Lead (existing, no changes)

```python
@dataclass
class Lead:
    title: str
    address: str
    phone_number: str
    website_url: str | None = None
    email: str | None = None
    tags: str | None = None
    source: str = ""  # "google_maps", "yelp", "twogis"
```

### SMTPConfig (new)

```python
@dataclass
class SMTPConfig:
    host: str = "smtp.gmail.com"
    port: int = 587
    email: str = ""
    password: str = ""  # App password
    use_tls: bool = True

    @classmethod
    def from_env(cls) -> "SMTPConfig":
        """Load from environment variables."""
        ...
```

### EmailTemplate (new)

```python
@dataclass
class EmailTemplate:
    subject: str  # "Hello {title}!"
    body: str     # "Dear {title}, we found you at {address}..."
    
    def render(self, lead: dict) -> tuple[str, str]:
        """Return (subject, body) with placeholders replaced."""
        ...
```

## API Contracts

### MCP Tools

**Tool: `search_leads`**
```json
{
  "name": "search_leads",
  "description": "Search for business leads using Google Maps or Yelp",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {"type": "string", "description": "Search query (e.g., 'restaurants')"},
      "location": {"type": "string", "description": "Location to search (e.g., 'Paris')"},
      "source": {"type": "string", "enum": ["google_maps", "yelp"], "default": "google_maps"}
    },
    "required": ["query", "location"]
  }
}
```

**Tool: `export_leads`**
```json
{
  "name": "export_leads",
  "description": "Export collected leads to a CSV file",
  "inputSchema": {
    "type": "object",
    "properties": {
      "filename": {"type": "string", "description": "Output filename", "default": "leads.csv"},
      "format": {"type": "string", "enum": ["csv"], "default": "csv"}
    }
  }
}
```

### Email Sender Interface

```python
class EmailSender(Protocol):
    async def send(
        self,
        to: str,
        subject: str,
        body: str,
    ) -> bool:
        """Send email, return True on success."""
        ...

class GmailSMTPSender:
    def __init__(self, config: SMTPConfig) -> None: ...
    async def send(self, to: str, subject: str, body: str) -> bool: ...
    async def send_bulk(self, leads: list[dict], template: EmailTemplate) -> list[bool]: ...
```

## Cleanup Tasks

### Files to Remove

| File/Folder | Reason |
|-------------|--------|
| `archived/` | Legacy code, no longer maintained |
| `py_lead_generation/requirements.txt` | Duplicate of pyproject.toml deps |
| `.github/workflows/python-publish.yml` | Duplicate of publish.yml |
| `setup.py` | Legacy setuptools, replaced by pyproject.toml |

### Files to Consolidate

| Current | Action |
|---------|--------|
| `publish.yml` + `python-publish.yml` | Keep `publish.yml` (uses uv), delete other |

### pyproject.toml Updates

Add new dependencies:
```toml
dependencies = [
    "beautifulsoup4>=4.12.0",
    "geopy>=2.4.0",
    "playwright>=1.40.0",
    "python-slugify>=8.0.0",
    "mcp>=1.0.0",  # NEW
]

[project.optional-dependencies]
email = []  # No extra deps needed, using stdlib
gui = []    # Tkinter is stdlib
```

Add entry points:
```toml
[project.scripts]
lead-gen-mcp = "py_lead_generation.src.mcp.server:main"
lead-gen-gui = "py_lead_generation.src.gui.app:main"
```

## Complexity Tracking

No constitution violations requiring justification. All changes follow established patterns.

## Dependencies Between User Stories

```
P1 (Package Cleanup) ─────┬────► P2 (MCP Server)
                          │
                          ├────► P3 (Email)
                          │
                          ├────► P4 (GUI)
                          │
                          └────► P5 (2GIS Interface)
```

P1 must be completed first as it establishes the clean foundation. P2-P5 can be implemented in parallel after P1.
