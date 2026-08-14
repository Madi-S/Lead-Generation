# py-lead-generation

A Python package for lead generation using web scraping. Collect business leads from Google Maps, Yelp, and more.

[![CI](https://github.com/Madi-S/Lead-Generation/actions/workflows/ci.yml/badge.svg)](https://github.com/Madi-S/Lead-Generation/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/py-lead-generation)](https://pypi.org/project/py-lead-generation/)
[![Python](https://img.shields.io/pypi/pyversions/py-lead-generation)](https://pypi.org/project/py-lead-generation/)

## Features

- 🔍 **Multiple Sources**: Google Maps, Yelp, 2GIS (coming soon)
- 📧 **Email Outreach**: Gmail SMTP integration with templates
- 🤖 **MCP Server**: Model Context Protocol for AI assistant integration
- ��️ **GUI Application**: Tkinter-based desktop app
- 📊 **CSV Export**: Export leads to CSV files
- ⚡ **Async-First**: Built with async/await for efficient scraping

## Installation

```bash
pip install py-lead-generation
```

Or install from source:

```bash
git clone https://github.com/Madi-S/Lead-Generation
cd Lead-Generation
pip install -e ".[dev]"
playwright install chromium
```

## Quickstart

### Python API

```python
import asyncio
from py_lead_generation import GoogleMapsEngine, YelpEngine

async def main() -> None:
    # Search Google Maps
    engine = GoogleMapsEngine("restaurants", "Paris", zoom=12)
    await engine.run()
    engine.save_to_csv("paris_restaurants.csv")
    print(f"Found {len(engine.entries)} leads")

    # Search Yelp
    engine = YelpEngine("Pizza", "New York")
    await engine.run()
    engine.save_to_csv("pizza_leads.csv")

if __name__ == "__main__":
    asyncio.run(main())
```

### GUI Application

Launch the desktop application:

```bash
lead-gen-gui
```

Or from Python:

```python
from py_lead_generation.src.gui import LeadGenerationApp

app = LeadGenerationApp()
app.run()
```

### MCP Server

Start the MCP server for AI assistant integration:

```bash
lead-gen-mcp
```

Available tools:
- `search_leads`: Search for business leads
- `export_leads`: Export leads to CSV
- `list_sources`: List available lead sources

### Email Outreach

Send personalized cold emails to collected leads:

```python
import asyncio
from py_lead_generation.src.email import (
    SMTPConfig,
    EmailTemplate,
    GmailSMTPSender,
)

async def send_emails():
    # Configure SMTP (use environment variables in production)
    config = SMTPConfig.from_env()
    sender = GmailSMTPSender(config)

    # Create email template
    template = EmailTemplate(
        subject="Partnership Opportunity - {title}",
        body="Dear {title},\n\nI found your business at {address}..."
    )

    # Send to leads
    leads = [
        {"title": "Acme Inc", "email": "contact@acme.com", "address": "123 Main St"},
    ]
    results = await sender.send_bulk(leads, template)
    print(f"Sent {sum(results)} emails successfully")

asyncio.run(send_emails())
```

## Environment Variables

Create a `.env` file (see `.env.example`):

```bash
# Gmail SMTP (for email outreach)
GMAIL_ADDRESS=your.email@gmail.com
GMAIL_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx

# MCP Server (optional)
MCP_HOST=localhost
MCP_PORT=8080
```

## Available Engines

| Engine | Source | Status |
|--------|--------|--------|
| `GoogleMapsEngine` | Google Maps | ✅ Working |
| `YelpEngine` | Yelp | ✅ Working |
| `TwoGisEngine` | 2GIS | 🚧 Interface only |

## Development

```bash
# Clone repository
git clone https://github.com/Madi-S/Lead-Generation
cd Lead-Generation

# Install with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/ -v

# Run linting
ruff check .
mypy py_lead_generation/
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.
